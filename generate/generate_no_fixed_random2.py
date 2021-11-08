import time
import tqdm
import random
import numpy as np
import expression as ep
import group as grp
from itertools import permutations
from sympy.utilities.iterables import multiset_permutations


N = 20
ep.reset_N(N)
id_perm = (range(N//2, N))
first_half_set = set(id_perm)
exclude_sets = [set([i]) for i in id_perm]
new_perm = []
left_terms = first_half_set
for p in range(N//2, N):
    retry = True
    while retry:
        retry = False
        cur_left_terms = tuple(left_terms - exclude_sets[p - N//2])
        if len(cur_left_terms) == 0:
            exit(0)
        q = random.choice(cur_left_terms)
        r = N + N//2 - 1 - p
        r_q = N + N//2 - 1 - q
        if r_q - N//2 < len(new_perm):
            k_r_q = new_perm[r_q - N//2]
            if k_r_q != r:
                exclude_sets[p - N//2].add(q)
                retry = True
                continue
        else:
            exclude_sets[r_q - N//2].add(r)
        left_terms.remove(q)
        new_perm.append(q)
        print(q)
print(new_perm)
