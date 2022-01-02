""" expression.py

Classes to represent a single expression,
batch of expressions with same number of terms and
batch of expressions with arbitrary number of terms.
"""
import os
import itertools
import numpy as np
import torch
import utils
from itertools import combinations

N_X = 8
ALPHABET = ["zero"] + ["x{}".format(x) for x in range(N_X)] + ["one"]
LEN_ALPHA = len(ALPHABET)
N_INPUT_X = 2**N_X  # number of possible values of X
# used to pack whole alphabet
EXP_ALPHA = np.logspace(
    0, LEN_ALPHA-1, LEN_ALPHA, base=2, dtype=np.int64)
EXP_X = np.logspace(
    0, LEN_ALPHA-3, LEN_ALPHA-2, base=2, dtype=np.int64)  # used to pack x


class Expr(object):
    """Class to represent a single expression.

    Attributes:
        mat: A boolean 2-d numpy array encoding the expression.
        n_terms: The number of terms in the expression.
        mask: A boolean 2-d numpy array for computation.
    """

    def __init__(self, str_expr="", mat=None):
        """ Init the expression with string or matrix

        Args:
            str_expr: A string contain the human-readable expression.
            mat: A boolean 2-d numpy array encoding the expression.
                Used to pass self.mat across instances of this class.
                Saves time for parsing str_expr.
        """
        # Init from string if no mat provided.
        if mat is None:
            terms = str_expr.split("+")
            n_terms = len(terms)
            # one-hot encoding:
            # row -> term
            # col -> character
            # True if the term has this character
            mat = np.zeros([n_terms, LEN_ALPHA], dtype=bool)
            for i, term in enumerate(terms):
                if ALPHABET[0] in term:
                    mat[i, 0] = True
                    continue
                elif ALPHABET[-1] in term:
                    mat[i, -1] = True
                    continue
                else:
                    chars = term.split("x")[1:]
                    chars = np.array(list(map(int, chars)))
                    mat[i, chars+1] = True
                    mat[i, -1] = True
                """
                for j, char in enumerate(ALPHABET):
                    if char in term:
                        mat[i, j] = True
                """
            # Every term implictly has char "one".
            # mat[:, -1] = True
        # Else use the passed mat.
        n_terms = len(mat)

        # Arrange mat.
        if n_terms > 0:
            # Remove the duplicate terms.
            # Convert to integer for summation later.
            mat = mat.astype(np.int64)
            uniq_arr, cnt = np.unique(
                mat, return_counts=True, axis=0
            )
            # Leave the terms appearing in odd times.
            mat = uniq_arr[cnt % 2 == 1]

            # Sort the terms for convenience in reading.
            # First compare the number of characters.
            # If equal, X0 < ... < Xi.
            mat_deg = mat.sum(axis=1)
            mat_exp = np.multiply(mat, EXP_ALPHA).sum(axis=1)
            arg_sort = np.lexsort((mat_exp, mat_deg))
            mat = mat[arg_sort].astype(bool)
        self.mat = mat
        self.n_terms = len(mat)
        # See __call__ for reason of inverse.
        self.mask = ~mat.astype(bool)

    def __call__(self, input_x: np.array):
        """ Compute the value of expression on the input x.

        Args:
            input_x: A 1d numpy array containing input value x
                    of size [N_INPUT_X].
                Or a 2-d numpy array containing batches of inputs
                    of size [batch, N_INPUT_X].
        """
        n_axis = len(input_x.shape)
        # Make the 1-d array to 2-d array
        # by setting batch = 1.
        if n_axis == 1:
            input_x = input_x[np.newaxis, :]

        # Repeat mask and input x
        # to compute at once.
        # For example:
        # mask = [x1, x0x2]
        # input_x = [x1=1, x0=x2=1]
        # ex_mask = [
        #   [x1, x0x2],
        #   [x1, x0x2],
        # ]
        # ex_input_x = [
        #   [x1=1, x1=1],
        #   [x0=x2=1, x0=x2=1],
        # ]
        batch_sz = len(input_x)
        ex_mask = np.repeat(np.expand_dims(
            self.mask, axis=0), batch_sz, axis=0)
        ex_input_x = np.repeat(np.expand_dims(
            input_x, axis=1), self.n_terms, axis=1)

        # Xor -> summation of terms.
        # And -> product of characters.
        # Or:
        # A term == 0 iff it has a character of value 0.
        # A term == 1 iff
        # it does **not** have this character (mask)
        # or the value of this character is 1 (input_x).
        #
        # For example:
        # term "x0x2" -> [0, 1, 0, 1, 1]
        # mask = [1, 0, 1, 0, 0]
        # input1 = [0, 1, 0, 1, 1] # x0=x2=1
        # mask | input1 = [1, 1, 1, 1, 1] # x0x2=1
        # input2 = [0, 1, 0, 0, 1] # x0=1, x2=0
        # mask | input2 = [1, 1, 1, 0, 1] # x0x2=0
        return np.bitwise_xor.reduce(
            np.bitwise_and.reduce(
                np.bitwise_or(ex_mask, ex_input_x), axis=2
            ), axis=1
        )

    def __add__(self, other):
        if isinstance(other, str):
            other = Expr(other)
        new_mat = np.concatenate([self.mat, other.mat], axis=0)
        return Expr(mat=new_mat)

    def __mul__(self, other):
        if isinstance(other, str):
            other = Expr(other)
        if len(self.mat) == 0:
            return Expr("zero")
        if len(other.mat) == 0:
            return Expr("zero")
        new_mat = []
        for p, q in itertools.product(self.mat, other.mat):
            new_mat.append(p | q)
        new_mat = np.stack(new_mat, axis=0)
        return Expr(mat=new_mat)

    def get_packed_x(self):
        """Get packed x.

        Returns:
            An integer 1-d numpy array of size [n_terms].
        """
        mat_x = self.mat[:, :-1]
        return utils.pack_arr_bits(mat_x)

    def get_pair_expr(self):
        """ Get pair expression

        x_i <-> x_(n-i)

        Returns:
            A paired Expr instance.
        """
        mat = np.copy(self.mat)
        mat_x = mat[:, 1:-1]
        mat[:, 1:-1] = mat_x[:, ::-1]
        return Expr("", mat)

    def is_pair_same(self):
        mat = np.copy(self.mat)
        mat_x = mat[:, 1:-1]
        return (mat_x == mat_x[:, ::-1]).all()

    def get_half_pair(self):
        mat = np.copy(self.mat)
        # mat_x = mat[:, 1:-1]
        first_half = mat[:, 1:N_X//2+1]
        second_half = mat[:, N_X//2+1:-1]
        mat[:, 1:N_X//2+1] = first_half[:, ::-1]
        mat[:, N_X//2+1:-1] = second_half[:, ::-1]
        return Expr("", mat)

    def get_first_half_pair(self):
        mat = np.copy(self.mat)
        first_half = mat[:, 1:N_X//2+1]
        mat[:, 1:N_X//2+1] = ~first_half
        return Expr("", mat)

    def get_second_half_pair(self):
        mat = np.copy(self.mat)
        second_half = mat[:, N_X//2+1:-1]
        mat[:, N_X//2+1:-1] = ~second_half
        return Expr("", mat)


    def get_all_out(self):
        """ Get output on all possible input.
        """
        return self.__call__(self.get_all_input())

    def test_balance(self):
        """ Test whether the output has equal number of 0/1.
        """
        out = self.get_all_out().astype(np.int64)
        return 2*out.sum() == out.size

    def get_all_input(self):
        """Get all possible input values.
        """
        input_x = np.zeros(
            [N_INPUT_X, LEN_ALPHA], dtype=bool)
        input_x[:, 0] = False  # "zero" = 0
        input_x[:, 1:-1] = utils.get_all_unpacked_bits(N_X)
        input_x[:, -1] = True  # "one" = 1
        return input_x

    def __repr__(self):
        """Get human readable string.
        """
        if len(self.mat) == 0:
            return "zero"
        list_str_terms = []
        for arr_term in self.mat:
            char_id = np.nonzero(arr_term)[0]
            if len(char_id) == 1:
                if char_id[0] == LEN_ALPHA - 1:  # only "one"
                    list_str_terms.append("one")
                elif char_id[0] == 0:
                    list_str_terms.append("zero")
                else:
                    list_str_terms.append(ALPHABET[char_id[0]])
            else:  # other characters exist, ignore "one"
                if 0 in char_id:
                    list_str_terms.append("zero")
                    continue
                # char_id[-1]: "one"
                list_str_chars = [ALPHABET[i] for i in char_id[:-1]]
                str_term = "".join(list_str_chars)
                list_str_terms.append(str_term)

        return "+".join(list_str_terms)

    def cpp_repr(self):
        """Get human readable string.
        """
        if len(self.mat) == 0:
            return "zero"
        list_str_terms = []
        for arr_term in self.mat:
            char_id = np.nonzero(arr_term)[0]
            if len(char_id) == 1:
                if char_id[0] == LEN_ALPHA - 1:  # only "one"
                    list_str_terms.append("one")
                elif char_id[0] == 0:
                    list_str_terms.append("zero")
                else:
                    list_str_terms.append(ALPHABET[char_id[0]])
            else:  # other characters exist, ignore "one"
                if 0 in char_id:
                    list_str_terms.append("zero")
                    continue
                # char_id[-1]: "one"
                list_str_chars = [ALPHABET[i] for i in char_id[:-1]]
                str_term = "*".join(list_str_chars)
                list_str_terms.append(str_term)

        return "+".join(list_str_terms)



class RegBatch(object):
    """Class to compute batch of expressions in a more effective way.

    It is okay to compute expressions one by one
    but it is more effective to compute them in batch.
    This class compute batch of expressions
    with the same number of terms.
    The limitation on the number of terms provides
    convenience and speed.
    It also has wide coverage
    because most expressions have similar numbers of term
    in the later search.

    Attributes:
        cache_t: Cached value of each term on each input.
        batch_sz: Batch size.
        n_terms: Number of terms.
        arr_exprs: A integer torch tensor encoding expressions.
    """

    def __init__(self, list_exprs: list):
        """Init with list of expressions of type string or Expr
        """
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        cache_t = torch.from_numpy(self.cache_terms()).to(device)
        if len(list_exprs) == 0:
            return
        if isinstance(list_exprs[0], str):
            list_exprs = [Expr(e) for e in list_exprs]

        list_n_terms = [e.n_terms for e in list_exprs]
        if min(list_n_terms) != max(list_n_terms):
            print("Only accept expressions with equal number of terms!")
            return

        batch_sz = len(list_exprs)
        n_terms = list_n_terms[0]
        arr_exprs = np.zeros([batch_sz, n_terms], dtype=np.int64)
        for i, expr in enumerate(list_exprs):
            arr_exprs[i] = Expr.get_packed_x(expr)
        arr_exprs = torch.from_numpy(arr_exprs).to(device)

        self.cache_t = cache_t
        self.batch_sz = batch_sz
        self.n_terms = n_terms
        self.arr_exprs = arr_exprs

    def run(self):
        """Get outputs on all possible inputs.

        Returns:
            A boolean torch tensor of size [batch, N_INPUT_X].
        """
        # Each element in arr_exprs means the code of a cached term.
        # Pick the output of terms from cache.
        res = self.cache_t[self.arr_exprs.flatten()]
        res = res.reshape(self.batch_sz, self.n_terms, N_INPUT_X)
        # Xor the terms
        res = torch.sum(res, dim=1) % 2
        return res.to(torch.bool)

    @staticmethod
    def cache_terms():
        """Cache the outputs of the terms on all possible inputs.
        """
        cache_file = "cache/cache_terms-{}.npy".format(N_X)
        if os.path.exists(cache_file):
            return np.load(cache_file)
        else:
            print("Cache...Please wait!")
            n_inputs = n_terms = N_INPUT_X
            cache_t = np.zeros([n_terms+1, n_inputs], dtype=bool)
            for i in range(n_terms):
                mat = np.zeros([1, LEN_ALPHA], dtype=bool)
                mat[0, 1] = False  # "zero" = 0
                mat[0, 1:-1] = utils.unpack_scale(i, N_X)
                mat[0, -1] = True  # "one" = 1
                expr = Expr("", mat)
                cache_t[i, :] = expr.get_all_out()
            cache_t[-1, :] = np.zeros([N_INPUT_X], dtype=bool)
            np.save(cache_file, cache_t)
            return cache_t


class ExprBatch():
    """Class to compute arbitrary expressions effectively.

    This class extends RegExpr and
    compute expressions with arbitrary number of terms.

    Attributes:
        list_reg_exprs: List of RegExpr instances for computation.
        list_inverse_ids: List of integer to restore the original order.
    """

    def __init__(self, list_exprs):
        if len(list_exprs) == 0:
            print("No expressions input!")
            return
        if isinstance(list_exprs[0], str):
            list_exprs = list(map(Expr, list_exprs))

        list_n_terms = np.array([e.n_terms for e in list_exprs])

        # Combine the expressions with the same numbers of terms.
        # Record index to restore the orders later.
        list_reg_exprs = []
        list_ids = []
        # For each number of terms.
        for n_terms in np.unique(list_n_terms):
            # Find all expressions with **n_terms** terms.
            new_list_id = (list_n_terms == n_terms).nonzero()[0]
            new_list_exprs = [list_exprs[i] for i in new_list_id]
            list_reg_exprs.append(new_list_exprs)
            list_ids.append(new_list_id)
        self.list_reg_exprs = list_reg_exprs

        # list_ids records the index in the original list.
        # list_reg_exprs[i] <-> list_exprs[list_ids[i]]
        # Inverse it to get output in original order.
        # list_reg_exprs[list_inverse_ids[i]] <-> list_exprs[i]
        list_ids = np.concatenate(list_ids, axis=0)
        list_inverse_ids = np.zeros_like(list_ids)
        for i, expr_id in enumerate(list_ids):
            list_inverse_ids[expr_id] = i
        self.list_inverse_ids = list_inverse_ids

    def run(self):
        """Get all output of RegExpr in original order.

        Returns:
            A torch tensor of size [batch, N_INPUT_X]
        """
        res = []
        for list_exprs in self.list_reg_exprs:
            reg_expr_batch = RegBatch(list_exprs)
            res.append(reg_expr_batch.run())
        res = torch.cat(res, dim=0)
        res = res[self.list_inverse_ids, :]
        return res


# TERMS = [
#     list(map(lambda x: "".join(x), combinations(ALPHABET[1:-1], i)))
#     for i in range(1, N_X)]
TERMS_BASE = ALPHABET[1:-1]
TERMS_FIRST_HALF = [
    list(map(lambda x: "".join(x), combinations(ALPHABET[1:N_X//2+1], i)))
    for i in range(2, N_X//2)]
TERMS_FIRST_HALF[0] = [
    e for e in zip(TERMS_FIRST_HALF[0][::2], TERMS_FIRST_HALF[0][::-2])]
TERMS_SECOND_HALF = [
    list(map(lambda x: "".join(x), combinations(ALPHABET[N_X//2+1:-1], i)))
    for i in range(2, N_X//2)]
TERMS_SECOND_HALF[0] = [
    e for e in zip(TERMS_SECOND_HALF[0][::2], TERMS_SECOND_HALF[0][::-2])]
TERMS_HIGH = [
    list(filter(lambda x: Expr(x).is_pair_same(),
                map(lambda x: "".join(x), combinations(ALPHABET[1:-1], N_X-2)))),
    list(map(lambda x: "".join(x), combinations(ALPHABET[1:-1], N_X-1)))
]

def reset_N(N):
    global N_X, ALPHABET, LEN_ALPHA, N_INPUT_X, EXP_ALPHA, EXP_X
    N_X = N
    ALPHABET = ["zero"] + ["x{}".format(x) for x in range(N_X)] + ["one"]
    LEN_ALPHA = len(ALPHABET)
    N_INPUT_X = 2**N_X  # number of possible values of X
    # used to pack whole alphabet
    EXP_ALPHA = np.logspace(
        0, LEN_ALPHA-1, LEN_ALPHA, base=2, dtype=np.int64)
    EXP_X = np.logspace(
        0, LEN_ALPHA-3, LEN_ALPHA-2, base=2, dtype=np.int64)  # used to pack x

    # global TERMS_BASE, TERMS_FIRST_HALF, TERMS_SECOND_HALF, TERMS_HIGH
    # # TERMS = [
    # #     list(map(lambda x: "".join(x), combinations(ALPHABET[1:-1], i)))
    # #     for i in range(1, N_X)]
    # TERMS_BASE = ALPHABET[1:-1]
    # TERMS_FIRST_HALF = [
    #     list(map(lambda x: "".join(x), combinations(ALPHABET[1:N_X//2+1], N_X//4))),
    #     list(map(lambda x: "".join(x), combinations(ALPHABET[1:N_X//2+1], N_X//2-1)))]
    # TERMS_FIRST_HALF[0] = [
    #     e for e in zip(TERMS_FIRST_HALF[0][::2], TERMS_FIRST_HALF[0][::-2])]
    # TERMS_SECOND_HALF = [
    #     list(map(lambda x: "".join(x), combinations(ALPHABET[N_X//2+1:-1], N_X//4))),
    #     list(map(lambda x: "".join(x), combinations(ALPHABET[N_X//2+1:-1], N_X//2-1)))]
    # TERMS_SECOND_HALF[0] = [
    #     e for e in zip(TERMS_SECOND_HALF[0][::2], TERMS_SECOND_HALF[0][::-2])]
    # TERMS_HIGH = [
    #     list(filter(lambda x: Expr(x).is_pair_same(),
    #                 map(lambda x: "".join(x), combinations(ALPHABET[1:-1], N_X-2)))),
    #     list(map(lambda x: "".join(x), combinations(ALPHABET[1:-1], N_X-1)))
    # ]


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
        list_exprs = [
            "x0",
            "x1x2+x3",
            "x1+x2+x3",
            "x3x4+x5",
        ]
        valid = []
        for expr in list_exprs:
            expr = Expr(expr)
            valid.append(expr.get_all_out())
        valid = np.array(valid)

        expr_batch = ExprBatch(list_exprs)
        test = expr_batch.run().numpy()
        if (valid == test).all():
            print("Right")
        list_exprs = [
            "x4+x4x5+x5x6"
        ]
        expr_batch = ExprBatch(list_exprs)
        test = expr_batch.run().long()
        print(test)
        e1 = Expr("zero+x1+zero+zero+x2")
        print(e1)
        e2 = Expr("zero+x1+zero+zero+x2+zero")
        print(e2)
        print(e1.get_all_out() == e2.get_all_out())
        """
        reset_N(12)
        print(N_X)
        print(TERMS_FIRST_HALF)
        print(TERMS_SECOND_HALF)
        # for e in combinations(TERMS_FIRST_HALF[0], 2):
        #     e = Expr("+".join(e))
        #     print(e)
            # print(e.test_balance())
        #     print(Expr(e).get_half_pair())
        # print(TERMS_SECOND_HALF)
        # print(TERMS_HIGH)

    main()
