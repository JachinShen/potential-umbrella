"""filter_selected.py
"""
import time
from itertools import permutations, product, chain
import torch
import numpy as np
import expression as ep


class AppendFilter(object):
    """Filter to select appended terms.

    Attributes:
        __append_terms: A list of strings to be appended on each expression.
        __standard: A torch tensor containing the outputs of permutation, used to test permutation.
        __grps: A list of strings containing candidate groups.
        __v_grps: A torch tensor storing output values of each group of size [batch, N_X, 2^N_X].
        __n_grp: Number of candidate groups.
        __cache_exprs: A list of strings containing combinations of __append_terms.
        __cache_paired_exprs: A list of strings containing paired combinations.
        __cache: A torch tensor storing output values of __cache_exprs.
        __paired_cache: A torch tensor storing output values of __cache_paired_exprs.
        __cache_shape: The shape of __append_terms.
        __res_print: A list storing found permutations.
    """
    __append_terms = [
        [
            "x0x1x2x3x4x5x6",
            "x0x1x2x3x4x5x7",
            "x0x1x2x3x4x6x7",
            "x0x1x2x3x5x6x7",
            "x0x1x2x4x5x6x7",
            "x0x1x3x4x5x6x7",
            "x0x2x3x4x5x6x7",
            "x1x2x3x4x5x6x7",
        ], [
            "x1x2x3x4x5x6",
            "x0x2x3x4x5x7",
            "x0x1x3x4x6x7",
            "x0x1x2x5x6x7",
        ],
    ]
    __standard = torch.arange(ep.N_INPUT_X, dtype=torch.int64)

    def __init__(self, list_grps):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        v_grps = []
        for group in list_grps:
            batch_expr = ep.ExprBatch(group)
            v_grps.append(batch_expr.run())
        v_grps = torch.stack(v_grps, dim=0)

        self.__grps = list_grps
        self.__v_grps = v_grps.to(device)
        self.__n_grp = len(list_grps)

        # Cache product of candidates in __append_terms.
        cache_shape = [len(t) for t in self.__append_terms]
        list_exprs = []
        list_paired_exprs = []
        for terms in product(*self.__append_terms):
            expr = ep.Expr("+".join(terms))
            expr_pair = expr.get_pair_expr()
            list_exprs.append(str(expr))
            list_paired_exprs.append(str(expr_pair))
        cache = ep.ExprBatch(list_exprs).run()
        paired_cache = ep.ExprBatch(list_paired_exprs).run()
        self.__cache_exprs = list_exprs
        self.__cache_paired_exprs = list_paired_exprs
        self.__cache = cache.to(device)
        self.__paired_cache = paired_cache.to(device)
        self.__cache_shape = cache_shape
        self.__standard = self.__standard.to(device)
        self.__res_print = []

    def run(self):
        """Run
        """
        for grp_id in range(self.__n_grp):
            print("[{}] Test group {}".format(time.time(), grp_id))
            self.test_grp(grp_id)
        return self.__res_print

    def test_grp(self, grp_id):
        """Test group
        """
        group = self.__grps[grp_id]
        out_grp = self.__v_grps[grp_id]
        batch_size = 10000
        list_ids = []
        cnt = 0
        # For each permutation (not combination) of __append_terms.
        # product(P(8, 4), P(4, 4))
        for ids in product(*[permutations(range(t), ep.N_X//2) for t in self.__cache_shape]):
            cnt += 1
            ids = list(ids)
            list_ids.append(ids)
            if cnt % batch_size == 0:
                if self.test_apd(out_grp, list_ids, group):
                    pass
                    #break
                list_ids = []
        if cnt % batch_size != 0:
            self.test_apd(out_grp, list_ids, group)

    def test_apd(self, out_grp, list_ids, group):
        """Test append terms

        Args:
            out_grp: A torch tensor storing output values of current group.
            list_ids: A list containing indexs of append terms to test.
            group: The string of current group.
        """
        arr_ids = self.__preprocess_ids(list_ids)
        out_apd = self.get_batch_apd_v(arr_ids)
        out = out_grp ^ out_apd
        is_perm = self.test_permutation(out)
        if is_perm.any():
            id_nonzero = is_perm.nonzero().cpu().flatten()
            found_apd_ids = arr_ids[id_nonzero].cpu().numpy()
            self.__store_found_perms(found_apd_ids, group)
            return True
        return False

    def __preprocess_ids(self, list_ids):
        # Extend the n-d index to 1-d index.
        arr_ids = torch.Tensor(list_ids).long()
        for i, len_t in enumerate(self.__cache_shape[1:]):
            arr_ids[:, i, :] *= len_t
        arr_ids = arr_ids.sum(dim=1)
        return arr_ids

    def get_batch_apd_v(self, arr_ids):
        """Get batch append value
        """
        batch_size = len(arr_ids)
        # For i-th append permutation, j-th expression, k-th output value:
        # ids[i, j]: candidate id of the j-th expression in the i-th append permutation.
        # res[i, j, k] = __cache[ids[i, j], k]
        res = ([self.__cache[arr_ids[:, i], :] for i in range(ep.N_X//2)] +
               [self.__paired_cache[arr_ids[:, i], :] for i in range(ep.N_X//2)[::-1]])
        res = torch.stack(res, dim=1)
        return res

    def __store_found_perms(self, found_apd_ids, group):
        """Store found permutations

        Args:
            found_apd_ids: A indexing numpy array of found append terms of size [found_size, N_X//2].
            group: A list of string containing the original group.
        """
        for id_grp_apd in found_apd_ids:
            str_grp = []
            for i, id_cache_term in enumerate(id_grp_apd):
                str_grp.append(
                    group[i] + self.__cache_exprs[id_cache_term])
            for i, id_cache_term in enumerate(id_grp_apd[::-1]):
                str_grp.append(
                    group[ep.N_X//2+i] + self.__cache_paired_exprs[id_cache_term])
            self.__res_print.append(";".join(str_grp))

    def test_permutation(self, res):
        """Test permutation according to the outputs.

        Args:
            res: A torch tensor storing the output values of many groups.
                Of size [batch, expressions, input_values]

        Returns:
            A boolean torch tensor indicating whether each group is permutation.
            Of size [batch].
        """
        res = res.long()
        # Convert bits to scales
        res = sum([res[:, i, :] << i for i in range(ep.N_X)])
        # A group is permutation iff sorted outputs exactly equal the standard outputs.
        res = res.sort(dim=1)[0]
        is_perm = (res == self.__standard).all(dim=1)
        return is_perm


def main():
    """Main
    """
    with open("half_permutations.txt", "r") as txt_file:
        str_perm = txt_file.read()
    list_str_grps = str_perm.split()
    list_grps = [len_t.split(";") for len_t in list_str_grps]
    append_filter = AppendFilter(list_grps)
    res = append_filter.run()
    print("Find {} permutations!".format(len(res)))
    with open("permutations.txt", "w") as txt_file:
        txt_file.write("\n".join(res))


if __name__ == "__main__":
    main()
