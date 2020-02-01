"""
Group of expression
"""

import time
import itertools
import torch
import numpy as np
import expression as ep


class Group():
    """
    Group of expression
    """
    pair_base_terms = ["x4", "x5", "x6", "x7"]

    def __init__(self, list_exprs: list):
        """
        Init with list of expressions
        """
        if len(list_exprs) == 0:
            print("No expression in the group!")
            return
        if isinstance(list_exprs[0], str):
            list_exprs = list(map(ep.Expr, list_exprs))
        for expr, p_term in zip(list_exprs[::-1], self.pair_base_terms):
            list_exprs.append(expr.get_pair_expr() + p_term)
        self.exprs = list_exprs

    def test_permutation(self):
        """
        Test whether the group of expressions is permutation
        """
        all_out = []
        for expr in self.exprs:
            all_out.append(expr.get_all_out())
        all_out_t = np.array(all_out).T
        all_out_merge = (all_out_t * ep.EXP_X).sum(axis=1)
        uniq_arr = np.unique(all_out_merge)
        return len(uniq_arr) == len(all_out_merge)

    def __repr__(self):
        """Print
        """
        list_str_grp = list(map(str, self.exprs))
        return "\t\n".join(list_str_grp)


class GroupBatch():
    """
    GroupBatch
    """
    pair_base_terms = ["x4", "x5", "x6", "x7"]
    n_expr = len(pair_base_terms)
    standard = torch.arange(ep.N_X, dtype=torch.int64)

    def __init__(self, list_grps):
        """Init"""
        if len(list_grps) == 0:
            print("No expression in the group!")
            return
        self.batch_size = len(list_grps)
        self.list_grps = list(map(self.preprocess_group, list_grps))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.standard = self.standard.to(device)

    def preprocess_group(self, list_exprs):
        """Preprocess"""
        if isinstance(list_exprs[0], str):
            list_exprs = list(map(ep.Expr, list_exprs))
        for expr, p_term in zip(list_exprs[::-1], self.pair_base_terms):
            list_exprs.append(expr.get_pair_expr() + p_term)
        return list_exprs

    def run(self):
        """Run"""
        list_exprs = list(itertools.chain(*self.list_grps))
        res = ep.ExprBatch(list_exprs).run()
        res = res.reshape(self.batch_size, 2*self.n_expr, -1).long()
        return res

    def test_permutation(self):
        """Test"""
        list_exprs = list(itertools.chain(*self.list_grps))
        res = ep.ExprBatch(list_exprs).run()
        res = res.reshape(self.batch_size, 2*self.n_expr, -1).long()
        res = sum([res[:, i, :] << i for i in range(ep.LEN_ALPHA-2)])
        res = res.sort(dim=1)[0]
        is_perm = (res == self.standard).all(dim=1)
        return is_perm


if __name__ == "__main__":
    def main():
        """Main
        """
        list_grps = [
            [
                "x4+x5x6+x5x7",
                "x5+x4x6+x4x7",
                "x6+x4x7+x5x7",
                "x7+x4x6+x5x6",
            ], [
                "x4+x4x5x6+x5x6x7",
                "x5+x5x6x7+x6x7x4",
                "x6+x6x7x4+x7x4x5",
                "x7+x7x4x5+x4x5x6"
            ]
        ]
        grp_batch = GroupBatch(list_grps)
        res = grp_batch.test_permutation()
        print(res.nonzero()[0][0])

    main()
