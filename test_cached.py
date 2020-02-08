"""
Test whether the cached expression group is permutation
"""

import time
from itertools import product
import torch
import group as grp
import expression as ep


class PermFilter():
    """PermFilter"""
    pair_base_terms = ["x4", "x5", "x6", "x7"]
    n_expr = len(pair_base_terms)
    standard = torch.arange(ep.N_X, dtype=torch.int64)

    def __init__(self):
        """Init"""
        with open("cached_balance_expression.txt", "r") as cache_file:
            str_cached = cache_file.read()
        str_cand = str_cached.split()
        expr_cand = [list(map(ep.Expr, expr.split("|")))
                     for expr in str_cand]
        expr_cand_pair = []
        v_cand = []
        v_cand_pair = []
        for p_term, y_cand in zip(self.pair_base_terms, expr_cand[::-1]):
            y_cand_pair = [expr.get_pair_expr() + p_term for expr in y_cand]
            expr_cand_pair.append(y_cand_pair)
        for y_cand in expr_cand:
            v_cand.append(ep.ExprBatch(y_cand).run())
        for y_cand_pair in expr_cand_pair:
            v_cand_pair.append(ep.ExprBatch(y_cand_pair).run())
        self.__v_cand = torch.stack(v_cand + v_cand_pair, dim=0)
        self.__expr_cand = expr_cand + expr_cand_pair
        self.__n_cand = len(self.__expr_cand[0])
        self.__n_y = 2 * len(str_cand)

    def run(self):
        """run"""
        cnt = 0
        batch_size = 10000
        list_ids = []
        for ids in product(*[list(range(self.__n_cand)) for i in range(self.__n_y // 2)]):
            cnt += 1
            ids = list(ids)
            list_ids.append(ids + ids[::-1])
            if cnt % batch_size == 0:
                print("[{}]: Have tested {} samples!".format(time.time(), cnt))
                if self.test(list_ids):
                    break
                list_ids = []
        if cnt % batch_size != 0:
            self.test(list_ids)

    def test(self, list_ids: list):
        """Test"""
        res = self.get_batch_grp_v(list_ids)
        is_perm = self.test_permutation(res)
        if is_perm.any():
            id_grps = is_perm.nonzero().cpu().flatten()
            print(id_grps)
            print_ids = [list_ids[i] for i in id_grps]
            for ids in print_ids:
                print(self.get_grp_expr(ids))
            return True
        return False

    def get_grp_expr(self, ids: list):
        """Get group expression"""
        return [self.__expr_cand[i][j] for i, j in zip(range(self.__n_y), ids)]

    def get_batch_grp_expr(self, list_ids: list):
        """Get batch group expression"""
        return [self.get_grp_expr(ids) for ids in list_ids]

    def get_grp_v(self, ids: list):
        """Get group value"""
        return torch.stack([self.__v_cand[i][j] for i, j in zip(range(self.__n_y), ids)], dim=0)

    def get_batch_grp_v(self, list_ids: list):
        """Get batch group value"""
        batch_size = len(list_ids)
        ids = torch.Tensor(list_ids).long()
        res = torch.zeros(batch_size, self.__n_y, ep.N_X, dtype=torch.bool)
        for i in range(self.__n_y):
            res[:, i, :] = self.__v_cand[i, ids[:, i], :]
        return res

    def test_permutation(self, res):
        """Test"""
        res = res.long()
        res = sum([res[:, i, :] << i for i in range(ep.LEN_ALPHA-2)])
        res = res.sort(dim=1)[0]
        is_perm = (res == self.standard).all(dim=1)
        return is_perm



def main():
    """Main
    """
    perm_filter = PermFilter()
    perm_filter.run()


if __name__ == "__main__":
    main()
