"""inverse.py
"""

import functools
import itertools

import numpy as np

import expression as ep
import utils


class Inverse(object):
    """Inverse

    Args:
        __expr_cache: A list of ep.Expr storing all the minimal terms.
        __all_input: A boolean numpy array storing bits of [0, 2^ep.N_X].
    """

    def __init__(self):
        self.__expr_cache = self.__cache_mini_terms()
        self.__all_input = utils.get_all_unpacked_bits(ep.N_X)
        self.contained_m_terms = []

    def run(self, group=[], truth_table=None, invert=True):
        """Run
        """
        if truth_table is None:
            group = ep.ExprBatch(group)
            truth_table = group.run().cpu().numpy()
        invert_table = self.__get_invert(truth_table)
        test_table = self.__get_invert(invert_table)
        print("Check permutation: {}".format(
            (test_table == truth_table).all()))
        if invert:
            self.__restore_expr(invert_table, invert)
        else:
            self.__restore_expr(truth_table, invert)

        m_terms = np.concatenate(self.contained_m_terms, axis=0)
        m_terms = np.multiply(m_terms, ep.EXP_ALPHA).sum(axis=1)
        m_terms = np.unique(m_terms)
        print("Cover {} minimium terms!".format(len(m_terms)))

    def __restore_expr(self, invert_table, invert=True):
        for i, out_x in enumerate(invert_table):
            mini_term_id = np.nonzero(out_x)[0]
            mini_terms = [self.__expr_cache[i] for i in mini_term_id]
            expr = functools.reduce(ep.Expr.__add__, mini_terms)
            print("Contain {} terms.".format(expr.n_terms))
            self.contained_m_terms.append(expr.mat)
            str_exrp = str(expr)
            if invert:
                str_exrp = str_exrp.replace("x", "y")
                print("x{}={}".format(i, str_exrp))
            else:
                print("y{}={}".format(i, str_exrp))

    @staticmethod
    def __cache_mini_terms():
        char_y = [ep.Expr("x{}".format(i)) for i in range(ep.N_X)]
        char_neg_y = [c+"one" for c in char_y]
        expr_cache = []
        # 01 -> (x0+1)x1
        for mini_t in itertools.product(*zip(char_neg_y, char_y)):
            expr = functools.reduce(ep.Expr.__mul__, mini_t)
            expr_cache.append(expr)
        return expr_cache

    def __get_invert(self, truth_table):
        """Get invert table from truth table.

        Args:
            truth_table: A numpy array of size [N_X, 2^N_X].
                i-th row, j-th col represents the value of y_i on input x,
                where x = [0, 1] for x0=0, x1=1, of size [N_X].
        """
        # i-th row, j-th col of invert table:
        # the value of x_i on input y,
        # where y = [0, 1] for y0=0, y1=1.
        # For j-th col of truth table,
        # the col-th col of invert table is j.
        invert_table = np.zeros_like(truth_table)
        # For x = [0, 1] and y = [1, 0]
        for input_x, out_y in zip(self.__all_input, truth_table.T):
            # invert_table[:, 1*2^1 + 0*2^0] = [[0], [1]]
            invert_table[:, utils.pack_bits(out_y)] = input_x.T
        return invert_table


def main():
    """Main
    """
    truth_table = np.load("sha256.npy")
    truth_table = np.expand_dims(truth_table, axis=1)
    truth_table = np.unpackbits(truth_table, axis=1).T
    inv = Inverse()
    inv.run(truth_table=truth_table)


if __name__ == "__main__":
    main()
