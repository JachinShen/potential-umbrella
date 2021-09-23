"""group.py

Classes to represent a group of equations.
"""

# import time
import itertools
import torch
import numpy as np
import expression as ep


class Group(object):
    """Class to represent a group of equations.

    Attributes:
        exprs: List of Expr instances.
    """

    def __init__(self, list_exprs: list):
        if len(list_exprs) == 0:
            print("No expression in the group!")
            return
        if isinstance(list_exprs[0], str):
            list_exprs = list(map(ep.Expr, list_exprs))
        self.exprs = list_exprs

    def test_permutation(self):
        """ Test whether the group of expressions is permutation.
        """
        # Collect output of each expression.
        all_out = []
        for expr in self.exprs:
            all_out.append(expr.get_all_out())
        # View the in the aspect of inputs and outputs of all expressions.
        # all_out = [expr_1, ..., expr_n]
        # all_out_t = [output_on_input_1, ..., output_on_input_m]
        all_out_t = np.array(all_out).T
        # Pack the outputs (bits) to scales to test permutation.
        all_out_merge = (all_out_t * ep.EXP_X).sum(axis=1)
        uniq_arr = np.unique(all_out_merge)
        return len(uniq_arr) == len(all_out_merge)

    def __repr__(self):
        list_str_grp = list(map(str, self.exprs))
        return "\t\n".join(list_str_grp)


class GroupBatch():
    """Class to represent batch of groups.

    Computer many groups effectively.

    Attributes:
        n_expr: Half of the number of expressions in one group.
        standard: A torch tensor containing the outputs of permutation,
            used to test permutation.
        batch_size: Number of groups.
        list_grps: List of groups.
    """
    standard = torch.arange(ep.N_INPUT_X, dtype=torch.int64)

    def __init__(self, list_grps):
        if len(list_grps) == 0:
            print("No expression in the group!")
            return
        self.batch_size = len(list_grps)
        self.list_grps = list(map(self.__preprocess_group, list_grps))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.standard = self.standard.to(device)

    def __preprocess_group(self, list_exprs):
        if isinstance(list_exprs[0], str):
            list_exprs = list(map(ep.Expr, list_exprs))
        return list_exprs

    def run(self):
        """Get the output of all groups
        """
        # View groups as many expressions.
        list_exprs = list(itertools.chain(*self.list_grps))
        res = ep.ExprBatch(list_exprs).run()
        res = res.reshape(self.batch_size, ep.N_X, -1).long()
        return res

    def test_permutation(self):
        """Test permutation of each group
        """
        res = self.run()
        # Convert outputs (bits) to scales.
        res = sum([res[:, i, :] << i for i in range(ep.N_X)])
        # The group is permutation iff
        #   the outputs cover the whole domain [0, 2^N_X].
        # Sort each group for convenience to compare with **standard**.
        # **standard** is the outputs [0, 2^N_X]
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
                "x0+x4+x1x2+x1x3",
                "x1+x5+x0x2+x0x3",
                "x2+x6+x0x3+x1x",
                "x3+x7+x0x2+x1x2",
            ], [
                "x4+x4x5x6+x5x6x7",
                "x5+x5x6x7+x6x7x4",
                "x6+x6x7x4+x7x4x5",
                "x7+x7x4x5+x4x5x6",
                "x0+x4+x0x2x3+x1x2x3",
                "x1+x5+x0x1x3+x0x2x3",
                "x2+x6+x0x1x2+x0x1x3",
                "x3+x7+x0x1x2+x1x2x3",
            ]
        ]
        grp_batch = GroupBatch(list_grps)
        res = grp_batch.test_permutation()
        print(res.nonzero()[0][0])

    main()
