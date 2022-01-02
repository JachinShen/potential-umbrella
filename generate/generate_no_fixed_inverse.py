import os
from itertools import permutations

import expression as ep
import group as grp
from inverse import Inverse

N = 12
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

def count_ops(func_name, list_eps):
    cpp_file = '''
void {func_name}(
    {x_args},
    {y_args}) {{
{eps}}}
    '''.format(
        func_name = func_name,
        x_args = ", ".join(["int x{}".format(i) for i in range(N)]),
        y_args = ", ".join(["int* y{}".format(i) for i in range(N)]),
        eps="".join(["\t*y{} = {};\n".format(i, e.cpp_repr()) for i, e in enumerate(list_eps)]))
    # print(cpp_file)

    with open("{}.cpp".format(func_name), "w") as file:
        file.write(cpp_file)

    os.system("g++ -O3 -S {0}.cpp -o {0}.asm".format(func_name))

    with open("{}.asm".format(func_name), "r") as file:
        asm_file = file.read()
        mul_cnt = asm_file.count("imull")
        add_cnt = asm_file.count("addl")

    return (mul_cnt, add_cnt)



basic_terms = dict()
basic_terms2 = dict()
basic_terms3 = dict()
for k in id_perm:
    basic_terms[k] = ep.Expr("x{}".format(k))
    basic_terms2[k] = ep.Expr("".join(["x{}".format(j)
                              for j in all_terms_set - {N+N//2-1-k}]))
    basic_terms3[k] = ep.Expr("".join(["x{}".format(j)
                              for j in all_terms_set - {k, N-1-k}]))

print("forward_add, forward_mul, backward_add, backward_mul")
full_perms = []
cnt = 0
for new_perm in permutations(range(N//2, N)):
    if fixed_point_perm(new_perm):
        continue

    if left_perm(new_perm):
        continue

    # cnt += 1
    # continue

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

    # print(first_half_eqs[0].cpp_repr())
    list_eps = first_half_eqs + second_half_eqs
    forward_add, forward_mul = (count_ops("forward", list_eps))

    inv = Inverse()
    list_inv_eps = inv.run(list_eps)
    backward_add, backward_mul = (count_ops("backward", list_inv_eps))

    # print("Forward: {}, backward: {}, ratio: {}".format(
    #     forward_add + forward_mul,
    #     backward_add + backward_mul,
    #     (backward_add + backward_mul) / (forward_add + forward_mul)))
    print(", ".join(map(str, (forward_add, forward_mul, backward_add, backward_mul))))

    # break

    # G = grp.Group(first_half_eqs + second_half_eqs)
    # # print(G)
    # # print(G.test_permutation())
    # # full_perms.append(str(G))
    # if G.test_permutation():
    #     print(new_perm)
    #     # print(G)
    # else:
    #     print(G)
    #     exit(0)
    cnt += 1
    # if cnt > 10:
    #     break
# print(cnt)
