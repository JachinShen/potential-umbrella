import expression as ep
import group as grp
import numpy as np
import re
from itertools import combinations, product

cand_eq = []
# idx = {
#     "x4": [],
#     "x5": [],
#     "x6": [],
#     "x7": [],
# }
# cnt = 0
for i, j in combinations(ep.TERMS_SECOND_HALF[0], 2):
    # print(i, j)
    ep1 = (ep.Expr(i[0]+"+one") * ep.Expr(j[0]+"+one") +
           ep.Expr(i[1]+"+one") * ep.Expr(j[1]+"+one"))
    id2 = (ep.Expr(i[0]+"+one") * ep.Expr(j[1]+"+one") +
           ep.Expr(i[1]+"+one") * ep.Expr(j[0]+"+one"))

    idx1 = []
    idx2 = []
    for k in range(4, 8):
        xk = "x{}".format(k)
        matches = (re.findall(xk, str(ep1)))
        if len(matches) == 3:
            idx1.append(k)
        matches = (re.findall(xk, str(id2)))
        if len(matches) == 3:
            idx2.append(k)

    # print(idx1)
    # print(ep1)
    # print(ep2)
    cand_eq.append([[ep1, idx1], [id2, idx2]])

print(cand_eq)

# for idx4 in idx["x4"]:
#     for idx5 in idx["x5"]:
#         for idx6 in idx["x6"]:
#             for idx7 in idx["x7"]:
#                 ep1 = ep.Expr("x4")+cand_eq[idx4[0]][idx4[1]]
#                 ep2 = ep.Expr("x5")+cand_eq[idx5[0]][idx5[1]]
#                 ep3 = ep.Expr("x6")+cand_eq[idx6[0]][idx6[1]]
#                 ep4 = ep.Expr("x7")+cand_eq[idx7[0]][idx7[1]]
#                 ep5 = ep.Expr("x0+x4")+cand_eq[idx7[0]][idx7[1]].get_pair_expr()
#                 ep6 = ep.Expr("x1+x5")+cand_eq[idx6[0]][idx6[1]].get_pair_expr()
#                 ep7 = ep.Expr("x2+x6")+cand_eq[idx5[0]][idx5[1]].get_pair_expr()
#                 ep8 = ep.Expr("x3+x7")+cand_eq[idx4[0]][idx4[1]].get_pair_expr()
#                 new_grp = [ep1, ep2, ep3, ep4, ep5, ep6, ep7, ep8]
#                 if (grp.Group(new_grp).test_permutation()):
#                     print("\n".join(map(str, new_grp)))
#                     print("====")

for cand1, cand2 in combinations(cand_eq, 2):
    for idxs in product(cand1[0][1], cand1[1][1], cand2[0][1], cand2[1][1]):
        # id1, id2, id3, id4 = idxs
        # print(idxs)
        uniq_idxs, uniq_inv = np.unique(idxs, return_inverse=True)
        if len(uniq_idxs) != 4:
            continue

        eq_list = [cand1[0][0], cand1[1][0], cand2[0][0], cand2[1][0]]
        print(idxs)
        # print(uniq_inv)
        print(eq_list)

        # ep1 = ep.Expr("x4")+eq_list[uniq_inv[0]]
        # ep2 = ep.Expr("x5")+eq_list[uniq_inv[1]]
        # ep3 = ep.Expr("x6")+eq_list[uniq_inv[2]]
        # ep4 = ep.Expr("x7")+eq_list[uniq_inv[3]]
        # ep5 = ep.Expr("x0+x4")+eq_list[uniq_inv[3]].get_pair_expr()
        # ep6 = ep.Expr("x1+x5")+eq_list[uniq_inv[2]].get_pair_expr()
        # ep7 = ep.Expr("x2+x6")+eq_list[uniq_inv[1]].get_pair_expr()
        # ep8 = ep.Expr("x3+x7")+eq_list[uniq_inv[0]].get_pair_expr()
        # new_grp = [ep1, ep2, ep3, ep4, ep5, ep6, ep7, ep8]
        # print(new_grp)
        # exit()

        new_grp = [
            "x4",
            "x5",
            "x6",
            "x7",
            "x0+x4",
            "x1+x5",
            "x2+x6",
            "x3+x7"
        ]
        new_grp = list(map(ep.Expr, new_grp))
        for i in range(4):
            new_grp[idxs[i]-4] += eq_list[i]
            new_grp[11-idxs[i]] += eq_list[i].get_pair_expr()
        # print(new_grp)
        print(grp.Group(new_grp).test_permutation())
        print("\n".join(map(str, new_grp)))
        print("====")


    # ep1 = (ep.Expr("x4")+i[0])
    # ep2 = (ep.Expr("x5")+i[1])
    # ep3 = (ep.Expr("x6")+j[0])
    # ep4 = (ep.Expr("x7")+j[1])
    # ep5 = (ep.Expr("x0+x4")+j[1].get_pair_expr())
    # ep6 = (ep.Expr("x1+x5")+j[0].get_pair_expr())
    # ep7 = (ep.Expr("x2+x6")+i[1].get_pair_expr())
    # ep8 = (ep.Expr("x3+x7")+i[0].get_pair_expr())
    # new_grp = [ep1, ep2, ep3, ep4, ep5, ep6, ep7, ep8]
    # print("\n".join(map(str, new_grp)))
    # print(grp.Group(new_grp).test_permutation())
    # print("====")
