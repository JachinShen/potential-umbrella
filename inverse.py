"""inverse.py
"""

import functools
import itertools
import operator

import numpy as np

import expression as ep
import utils


class Inverse(object):
    """Inverse
    """

    def __init__(self):
        self.__expr_cache = self.__cache_mini_terms()
        self.__all_input = utils.get_all_unpacked_bits(ep.N_X)

    def run(self, group):
        """Run
        """
        group = ep.ExprBatch(group)
        truth_table = group.run().numpy()
        invert_table = self.__get_invert(truth_table)
        self.__restore_expr(invert_table)


    def __restore_expr(self, invert_table):
        for i, out_x in enumerate(invert_table):
            mini_term_id = np.nonzero(out_x)[0]
            mini_terms = [self.__expr_cache[i] for i in mini_term_id]
            expr = functools.reduce(ep.Expr.__add__, mini_terms)
            print(expr)


    @staticmethod
    def __cache_mini_terms():
        char_y = [ep.Expr("x{}".format(i)) for i in range(ep.N_X)]
        char_neg_y = [c+"one" for c in char_y]
        expr_cache = []
        for mini_t in itertools.product(*zip(char_neg_y, char_y)):
            expr = functools.reduce(ep.Expr.__mul__, mini_t)
            expr_cache.append(expr)
        return expr_cache


    def __get_invert(self, truth_table):
        invert_table = np.zeros_like(truth_table)
        for input_x, out_y in zip(self.__all_input, truth_table.T):
            invert_table[:, utils.pack_bits(out_y)] = input_x.T
        return invert_table


def main():
    """Main
    """
    with open("half_permutations.txt", "r") as txt_file:
        str_perm = txt_file.read()
    list_str_grps = str_perm.split()
    list_grps = [len_t.split(";") for len_t in list_str_grps]
    inv = Inverse()
    for group in list_grps:
        inv.run(group)


if __name__ == "__main__":
    main()
