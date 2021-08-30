from itertools import combinations, permutations, islice


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    seq = list(seq)
    seq += seq[:n-1]
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


N_X = 8
HALF_N_X = N_X // 2
QUATER_N_X = N_X // 4
terms_second_n_min_1 = ["x"+"x".join(map(str, order)) for order in window(
    range(HALF_N_X, N_X), HALF_N_X-1)]
# terms_second_n_min_1 = ["".join(t) for t in combinations(
# ["x{}".format(i) for i in range(HALF_N_X, N_X)], HALF_N_X-1)]

terms_first_n_div_4 = ["".join(t) for t in combinations(
    ["x{}".format(i) for i in range(HALF_N_X)], QUATER_N_X)]
terms_second_n_div_4 = ["".join(t) for t in combinations(
    ["x{}".format(i) for i in range(HALF_N_X, N_X)], QUATER_N_X)]

print(terms_second_n_min_1)
print(terms_first_n_div_4)
print(terms_second_n_div_4)

# block_second_n_min_1 = ["+".join(i)
# for i in combinations(terms_second_n_min_1, 2)]
block_second_n_min_1 = ["+".join(i) for i in window(terms_second_n_min_1, 2)]
block_first_n_div_4 = ["+".join([i, j])
                       for i, j in zip(terms_first_n_div_4, terms_first_n_div_4[::-1])]
block_second_n_div_4 = ["+".join([i, j])
                        for i, j in zip(terms_second_n_div_4, terms_second_n_div_4[::-1])]
block_first_n_div_4 = block_first_n_div_4[:len(block_first_n_div_4)//2]
block_second_n_div_4 = block_second_n_div_4[:len(block_second_n_div_4)//2]
print(block_second_n_min_1)
print(block_first_n_div_4)
print(block_second_n_div_4)


def terms_in(T1, T2):
    N1 = T1.split("x")
    N2 = T2.split("x")
    for i in N2:
        if i not in N1:
            return False
    return True


dict_feasible = dict()
for sum_n_min_1 in block_second_n_min_1:
    term_container = sum_n_min_1.split("+")
    for sum_n_div_4 in block_second_n_div_4:
        term_elem = sum_n_div_4.split("+")
        # print(terms_in(term_container[0], term_elem[0]))
        flag = ((terms_in(term_container[0], term_elem[0])
                and terms_in(term_container[1], term_elem[1]))

                or (terms_in(term_container[1], term_elem[0])
                and terms_in(term_container[0], term_elem[1])))
        # print(sum_n_min_1, sum_n_div_4, flag)
        if flag:
            v = dict_feasible.get(sum_n_min_1)
            if v is None:
                dict_feasible[sum_n_min_1] = [sum_n_div_4]
            else:
                dict_feasible[sum_n_min_1].append(sum_n_div_4)

print(dict_feasible)


L_n_min_1 = len(terms_second_n_min_1)
# for begin in range(L_n_min_1):
# order = [begin, (begin+1) % L_n_min_1, (begin+2) % L_n_min_1, (begin+3) % 4, (begin+4) % 4]
for order in window(block_second_n_min_1, 4):
    # print(order)
    T_n_min_1 = [
        "x4+" + order[0],
        "x5+" + order[1],
        "x6+" + order[2],
        "x7+" + order[3],
    ]
    print("========================")
    print(T_n_min_1)
    # print(dict_feasible[T_n_min_1[0]])
    # print(dict_feasible[T_n_min_1[1]])
