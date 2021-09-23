import expression as ep
import group as grp
import numpy as np
import re
from itertools import combinations, product

ep.reset_N(12)
N_X = ep.N_X
HALF_N = N_X // 2

cand_eq = []
# print(ep.TERMS_SECOND_HALF)
for i, j in combinations(ep.TERMS_SECOND_HALF[0], 2):
    # print(i, j)
    ep1 = (ep.Expr(i[0]+"+one") * ep.Expr(j[0]+"+one") +
           ep.Expr(i[1]+"+one") * ep.Expr(j[1]+"+one"))
    ep2 = (ep.Expr(i[0]+"+one") * ep.Expr(j[1]+"+one") +
           ep.Expr(i[1]+"+one") * ep.Expr(j[0]+"+one"))

    idx1 = []
    idx2 = []
    for k in range(HALF_N, N_X):
        xk = "x{}".format(k)
        matches = (re.findall(xk, str(ep1)))
        if len(matches) == 3:
            idx1.append(k)
        matches = (re.findall(xk, str(ep2)))
        if len(matches) == 3:
            idx2.append(k)

    # print(idx1)
    # print(ep1)
    # print(ep2)
    cand_eq.append([[ep1, idx1], [ep2, idx2]])

print(cand_eq)
for cands in combinations(cand_eq, N_X//4):
    idx_list = []
    eq_list = []
    for i in range(N_X//4):
        idx_list.append(cands[i][0][1])
        idx_list.append(cands[i][1][1])
        eq_list.append(cands[i][0][0])
        eq_list.append(cands[i][1][0])
    # print(idx_list)
    for idxs in product(*idx_list):
        # id1, id2, id3, id4 = idxs
        # print(idxs)
        uniq_idxs, uniq_inv = np.unique(idxs, return_inverse=True)
        if len(uniq_idxs) != N_X//2:
            continue

        # eq_list = [cand1[0][0], cand1[1][0], cand2[0][0], cand2[1][0]]
        print(idxs)
        # print(uniq_inv)
        # print(eq_list)

        new_grp = ["x{}".format(i) for i in range(HALF_N, N_X)]
        new_grp += ["x{}+x{}".format(i-HALF_N, i) for i in range(HALF_N, N_X)]
        new_grp = list(map(ep.Expr, new_grp))
        for i in range(HALF_N):
            new_grp[idxs[i]-HALF_N] += eq_list[i]
            new_grp[N_X-1-(idxs[i]-HALF_N)] += eq_list[i].get_pair_expr()
        # print(new_grp)
        if (grp.Group(new_grp).test_permutation()):
            print("\n".join(map(str, new_grp)))
            print("====")
