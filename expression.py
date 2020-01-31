"""
Expression.py
"""
import os
import numpy as np
import torch
from utils import *

ALPHABET = ["zero", "x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "one"]
LEN_ALPHA = len(ALPHABET)
N_X = 2**(LEN_ALPHA - 2)
EXP = np.logspace(0, LEN_ALPHA-1, LEN_ALPHA, base=2, dtype=np.int64)
EXP_X = np.logspace(0, LEN_ALPHA-3, LEN_ALPHA-2, base=2, dtype=np.int64)


class Expression():
    """
    Expression class
    """

    def __init__(self, str_expr="", mat=None):
        """
        Read string of expression

        Arguments
        ------
        s:String
            Human readable expression
        """
        if mat is not None:
            self.mat = mat
        else:
            terms = str_expr.split("+")
            n_terms = len(terms)
            self.mat = np.zeros([n_terms, LEN_ALPHA], dtype=np.bool)
            for i, term in enumerate(terms):
                for j, char in enumerate(ALPHABET):
                    if char in term:
                        self.mat[i, j] = True
            self.mat[:, -1] = True
        self.n_terms = len(self.mat)
        if self.n_terms > 0:
            mat = self.mat.astype(np.int64)
            uniq_arr, cnt = np.unique(
                mat, return_counts=True, axis=0
            )
            mat = uniq_arr[cnt % 2 == 1]
            mat_deg = mat.sum(axis=1)
            mat_exp = np.multiply(mat, EXP).sum(axis=1)
            arg_sort = np.lexsort((mat_exp, mat_deg))
            self.mat = mat[arg_sort].astype(np.bool)
        self.mask = ~self.mat.astype(np.bool)

    def __call__(self, value):
        n_axis = len(value.shape)
        if n_axis == 1:  # make batch size = 1
            value = value[np.newaxis, :]
        batch_sz = len(value)
        ex_mask = np.repeat(np.expand_dims(
            self.mask, axis=0), batch_sz, axis=0)
        ex_v = np.repeat(np.expand_dims(value, axis=1), self.n_terms, axis=1)
        return np.bitwise_xor.reduce(
            np.bitwise_and.reduce(
                np.bitwise_or(ex_mask, ex_v), axis=2
            ), axis=1
        )

    def __add__(self, other):
        if isinstance(other, str):
            other = Expression(other)
        new_mat = np.concatenate([
            self.mat, other.mat
        ], axis=0)
        return Expression("", new_mat)

    def get_packed_mat(self):
        mat = self.mat[:, 1:-1]
        return pack_arr(mat)

    def get_pair_expr(self):
        """
        Return pair expression

        x0 -> x7
        """
        mat = np.copy(self.mat)
        x_mat = mat[:, 1:-1]
        mat[:, 1:-1] = x_mat[:, ::-1]
        return Expression("", mat)

    def get_all_out(self):
        """
        Get output on all possible input.
        """
        return self.__call__(self.get_all_value())

    def test_balance(self):
        """
        Test whether the output has equal number of 0/1
        """
        all_value = self.get_all_value()
        out = self.__call__(all_value).astype(np.int64)
        sum_out = out.sum()
        return sum_out * 2 == out.size

    def get_all_value(self):
        """
        Give all possible value
        """
        all_value = np.zeros(
            [2**(LEN_ALPHA - 2), LEN_ALPHA], dtype=np.bool)
        all_value[:, 0] = False
        all_value[:, 1:-1] = get_all_unpacked_bits(LEN_ALPHA - 2)
        all_value[:, -1] = True
        return all_value

    def __repr__(self):
        """
        Print human readable expression.
        """
        arr_expr = []
        for arr_term in self.mat:
            exist_chars_id = np.nonzero(arr_term)[0]
            if len(exist_chars_id) == 1 and exist_chars_id[0] == LEN_ALPHA - 1:
                # only one
                arr_expr.append("one")
            else:
                # other characters exist, ignore one
                exist_chars = [ALPHABET[i] for i in exist_chars_id[:-1]]
                str_term = " ".join(exist_chars)
                arr_expr.append(str_term)

        return " + ".join(arr_expr)


class RegExprBatch():
    """
    Compute batch of expressions in a more effective way.
    """

    def __init__(self, list_exprs):
        """
        Init with list of expressions
        """
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        cache_t = torch.from_numpy(self.cache_terms()).to(device)
        if len(list_exprs) == 0:
            return
        if isinstance(list_exprs[0], str):
            list_exprs = [Expression(e) for e in list_exprs]

        list_n_terms = [e.n_terms for e in list_exprs]
        if min(list_n_terms) != max(list_n_terms):
            print("Only accept expressions with equal number of terms!")
            return
        batch_sz = len(list_exprs)
        n_terms = list_n_terms[0]
        arr_exprs = np.zeros([batch_sz, n_terms], dtype=np.int64)
        for i, expr in enumerate(list_exprs):
            arr_exprs[i] = expr.get_packed_mat()

        #cache_t = cache_t.expand(batch_sz, N_X, N_X)
        arr_exprs = torch.from_numpy(arr_exprs).to(device)
        #arr_exprs = arr_exprs.expand(batch_sz, N_X, n_terms)
        # print(arr_exprs)

        self.cache_t = cache_t
        self.batch_sz = batch_sz
        self.n_terms = n_terms
        self.arr_exprs = arr_exprs

    def run(self):
        """
        Run
        """
        res = self.cache_t[self.arr_exprs.flatten()].reshape(
            self.batch_sz, self.n_terms, N_X)
        res = torch.sum(res, dim=1) % 2
        return res.to(torch.bool)

    @staticmethod
    def cache_terms():
        """
        Cache terms
        """
        cache_file = "cache_terms-{}.npy".format(LEN_ALPHA)
        if os.path.exists(cache_file):
            return np.load(cache_file)
        else:
            n_values = n_terms = N_X
            cache_t = np.zeros([n_terms, n_values], dtype=np.bool)
            for i in range(n_terms):
                mat = np.zeros([1, LEN_ALPHA], dtype=np.bool)
                mat[0, 1:-1] = unpack_elem(i, LEN_ALPHA-2)
                mat[0, -1] = True
                expr = Expression("", mat)
                # print(e)
                # print(e.get_all_out().astype(np.int))
                cache_t[i, :] = expr.get_all_out()
            np.save(cache_file, cache_t)
            return cache_t

class ExprBatch():
    """
    ExprBatch
    """
    def __init__(self, list_exprs):
        if len(list_exprs) == 0:
            return
        if isinstance(list_exprs[0], str):
            list_exprs = list(map(Expression, list_exprs))

        list_n_terms = np.array([e.n_terms for e in list_exprs])

        list_reg_exprs = []
        list_ids = []
        for n_terms in np.unique(list_n_terms):
            new_list_id = (list_n_terms == n_terms).nonzero()[0]
            new_list_exprs = [list_exprs[i] for i in new_list_id]
            list_reg_exprs.append(new_list_exprs)
            list_ids.append(new_list_id)
        self.list_reg_exprs = list_reg_exprs

        list_ids = np.concatenate(list_ids, axis=0)
        list_inverse_ids = np.zeros_like(list_ids)
        for i, expr_id in enumerate(list_ids):
            list_inverse_ids[expr_id] = i
        self.list_inverse_ids = list_inverse_ids

    def run(self):
        """
        Run
        """
        res = []
        for list_exprs in self.list_reg_exprs:
            reg_expr_batch = RegExprBatch(list_exprs)
            res.append(reg_expr_batch.run())
        res = torch.cat(res, dim=0)
        res = res[self.list_inverse_ids, :]
        return res

if __name__ == "__main__":
    def main():
        """
        Main
        """
        """
        EXPR = Expression("x4x5+x5x6+x5x7+x4+x0x1x2x3x4x5x6x7")
        print(EXPR.get_packed_mat())
        print(EXPR(EXPR.get_all_value()).astype(np.int))
        print(EXPR.test_balance())
        rint(EXPR + "x2x3 + x3")
        expr_batch = RegExprBatch(list_exprs)
        test = expr_batch.run().numpy()
        if (valid == test).all():
            print("Right")
        """
        list_exprs = [
            "x0",
            "x1x2+x3",
            "x1+x2+x3",
            "x3x4+x5",
        ]
        valid = []
        for expr in list_exprs:
            expr = Expression(expr)
            valid.append(expr.get_all_out())
        valid = np.array(valid)

        expr_batch = ExprBatch(list_exprs)
        test = expr_batch.run().numpy()
        if (valid == test).all():
            print("Right")

    main()
