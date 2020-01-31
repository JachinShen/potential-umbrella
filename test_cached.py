"""
Test whether the cached expression group is permutation
"""

import time
from itertools import product
import group as grp


def main():
    """Main
    """
    with open("cached_balance_expression.txt", "r") as cache_file:
        str_cached = cache_file.read()
    cand_expr = str_cached.split()
    cand_grp = [expr.split("|") for expr in cand_expr]
    print("Start testing...")
    cnt = 0
    list_grps = []
    for exprs in product(*cand_grp):
        cnt += 1
        list_grps.append(list(exprs))
        if cnt % 100 == 0:
            print("[{}]: Have tested {} samples!".format(time.time(), cnt))
            grp_batch = grp.GroupBatch(list_grps)
            res = grp_batch.test_permutation()
            if res.any():
                print(cnt, res.nonzero())
                break
            break


if __name__ == "__main__":
    main()
