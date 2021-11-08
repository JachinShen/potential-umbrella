from torch._C import set_num_interop_threads
import expression as ep
import group as grp
from itertools import permutations


N = 24
ep.reset_N(N)
id_perm = range(N//2, N)
first_half_set = set(id_perm)
all_terms_set = set(range(N))
# basic_terms = [ep.Expr("x{}".format(i)) for i in id_perm]
# basic_terms2 = [ep.Expr("".join([
#     "x{}".format(j) for j in all_terms_set - {i}]))
#     for i in id_perm[::-1]]
# basic_terms3 = [ep.Expr("".join([
#     "x{}".format(j) for j in all_terms_set - {i, N-1-i}]))
#     for i in id_perm]


def fixed_point_perm(perm):
    for e1, e2 in zip(perm, id_perm):
        if e1 == e2:
            return True
    return False


def left_perm(new_perm):
    for p, pi2 in zip(id_perm, new_perm):
        j = N + N//2 - 1 - p
        k_set = first_half_set - {p, pi2, j}
        k_17_set = set([N + N//2 - 1 - i for i in k_set])
        pi2_k_17_set = set([new_perm[i-N//2] for i in k_17_set])
        if j in pi2_k_17_set:
            return True
    return False


basic_terms = dict()
basic_terms2 = dict()
basic_terms3 = dict()
for k in id_perm:
    basic_terms[k] = ep.Expr("x{}".format(k))
    basic_terms2[k] = ep.Expr("".join(["x{}".format(j)
                              for j in all_terms_set - {N+N//2-1-k}]))
    basic_terms3[k] = ep.Expr("".join(["x{}".format(j)
                              for j in all_terms_set - {k, N-1-k}]))

# half_perms = []
# cnt = 0
# for new_perm in permutations(range(N//2, N)):
#     if fixed_point_perm(new_perm, id_perm):
#         continue
#     print(new_perm)
#     first_half_eqs = []
#     for t1, t2 in zip(id_perm, new_perm):
#         left_terms = first_half_set - {t1, t2}
#         equation = basic_terms[t1] + (
#             ep.Expr("x{}+x{}".format(t1, t2)) *
#             ep.Expr("".join(["x{}".format(i) for i in left_terms]))
#         )
#         # print(equation)
#         first_half_eqs.append(equation)
#     second_half_eqs = []
#     for t, equation in zip(id_perm, first_half_eqs):
#         pair_eq = basic_terms[t] + equation.get_pair_expr()
#         second_half_eqs.append(pair_eq)

#     G = grp.Group(first_half_eqs + second_half_eqs)
#     assert(G.test_permutation())
#     half_perms.append(str(G))
#     cnt += 1
#     if cnt > 20:
#         break
# # print(half_perms)
# half_perms_set = set(half_perms)

print("Full:")
full_perms = []
cnt = 0
for new_perm in permutations(range(N//2, N)):
    if fixed_point_perm(new_perm):
        continue

    if left_perm(new_perm):
        continue

    cnt += 1 
    continue

    first_half_eqs = []
    for t1, t2 in zip(id_perm, new_perm):
        left_terms = first_half_set - {t1, t2}
        equation = basic_terms[t1] 
        equation += (
            ep.Expr("x{}+x{}".format(t1-N//2, t2-N//2)) *
            ep.Expr("+".join(["x{}".format(i-N//2) for i in left_terms])))
        equation += (
            ep.Expr("x{}+x{}".format(t1, t2)) *
            ep.Expr("".join(["x{}".format(i) for i in left_terms]))
        ) + basic_terms2[t1] + basic_terms3[t2]
        # print(equation)
        first_half_eqs.append(equation)
    second_half_eqs = []
    for t, equation in zip(id_perm, first_half_eqs[::-1]):
        pair_eq = basic_terms[t] + equation.get_pair_expr()
        second_half_eqs.append(pair_eq)

    G = grp.Group(first_half_eqs + second_half_eqs)
    # print(G)
    # print(G.test_permutation())
    # full_perms.append(str(G))
    if G.test_permutation():
        print(new_perm)
        # print(G)
    else:
        print(G)
        exit(0)
    cnt += 1
    # if cnt > 10:
    #     break
print(cnt)
