"""Select permutation from cached expressions.
"""

import time
from itertools import product
import torch
import expression as ep


class PermFilter(object):
    """Handle all things about selection.

    Attributes:
        orth_terms: Terms to make the permutation orthogonal.
        n_expr: Half of the number of expressions in one group.
        standard: A torch tensor containing the outputs of permutation, used to test permutation.
        __v_cand: A torch tensor storing the output values of every candidate expression.
        __expr_cand: A list of candidate expressions.
        __n_cand: Number of candidates for each expression.
        __n_y: Number of y in "y = f(x)".

    """
    orth_terms = ["x{}".format(i) for i in range(ep.N_X//2, ep.N_X)]
    n_expr = len(orth_terms)
    standard = torch.arange(ep.N_INPUT_X, dtype=torch.int64)

    def __init__(self):
        with open("cached_balance_expression.txt", "r") as cache_file:
            str_cached = cache_file.read()
        str_cands_expr = str_cached.split()
        expr_cand = [list(map(ep.Expr, expr.split("|")))
                     for expr in str_cands_expr]
        expr_cand_pair = []
        v_cand = []
        v_cand_pair = []
        # Append pair expression for each candidate.
        for p_term, y_cand in zip(self.orth_terms, expr_cand[::-1]):
            y_cand_pair = [expr.get_pair_expr() + p_term for expr in y_cand]
            expr_cand_pair.append(y_cand_pair)
        # Cache output values for original candidates.
        for y_cand in expr_cand:
            v_cand.append(ep.ExprBatch(y_cand).run())
        # Cache output values for paired candidates.
        for y_cand_pair in expr_cand_pair:
            v_cand_pair.append(ep.ExprBatch(y_cand_pair).run())
        self.__v_cand = torch.stack(v_cand + v_cand_pair, dim=0)
        self.__expr_cand = expr_cand + expr_cand_pair
        self.__n_cand = len(self.__expr_cand[0])
        self.__n_y = 2 * len(str_cands_expr)

    def run(self):
        """Select and print found permutations.
        """
        cnt = 0
        batch_size = 10000
        list_ids = []
        # Try every combination of candidates.
        for ids in product(*[list(range(self.__n_cand)) for i in range(self.__n_y // 2)]):
            cnt += 1
            ids = list(ids)
            # The second half is determined by the first half.
            list_ids.append(ids + ids[::-1])
            if cnt % batch_size == 0:
                print("[{}]: Have tested {} samples!".format(time.time(), cnt))
                if self.test(list_ids):
                    break
                list_ids = []
        # If the left combinations is not tested.
        if cnt % batch_size != 0:
            self.test(list_ids)

    def test(self, list_ids: list):
        """Test the permutation of batched groups.
        """
        res = self.get_batch_grp_v(list_ids)
        is_perm = self.test_permutation(res)
        if is_perm.any():
            id_grps = is_perm.nonzero().cpu().flatten()
            print(id_grps)
            print_ids = [list_ids[i] for i in id_grps]
            with open("permutations.txt", "w") as txt_file:
                for ids in print_ids:
                    grp = self.get_grp_expr(ids)
                    str_grp = list(map(str, grp))
                    txt_file.write("\n".join(str_grp))
                    txt_file.write("\n===\n")
            return True
        return False

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
        is_perm = (res == self.standard).all(dim=1)
        return is_perm

    def get_grp_expr(self, ids: list):
        """Get group expression
        """
        return [self.__expr_cand[i][j] for i, j in zip(range(self.__n_y), ids)]

    def get_batch_grp_expr(self, list_ids: list):
        """Get batch group expression
        """
        return [self.get_grp_expr(ids) for ids in list_ids]

    def get_grp_v(self, ids: list):
        """Get group value
        """
        return torch.stack(
            [self.__v_cand[i][j] for i, j in zip(range(self.__n_y), ids)],
            dim=0)

    def get_batch_grp_v(self, list_ids: list):
        """Get batch group value
        """
        batch_size = len(list_ids)
        ids = torch.Tensor(list_ids).long()
        res = torch.zeros(batch_size, self.__n_y,
                          ep.N_INPUT_X, dtype=torch.bool)
        # For i-th group, j-th expression, k-th output value:
        # ids[i, j]: candidate id of the j-th expression in the i-th group.
        # res[i, j, k] = __v_cand[j, ids[i, j], k]
        for i in range(self.__n_y):
            res[:, i, :] = self.__v_cand[i, ids[:, i], :]
        return res


def main():
    """Main
    """
    perm_filter = PermFilter()
    perm_filter.run()


if __name__ == "__main__":
    main()
