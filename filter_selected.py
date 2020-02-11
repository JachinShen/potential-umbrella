"""filter_selected.py
"""
from itertools import permutations
import numpy as np
import expression as ep
import group as grp

def main():
    """Main
    """
    list_n_1_terms = [
        "x0x1x2x3x4x5x6",
        "x0x1x2x3x4x5x7",
        "x0x1x2x3x4x6x7",
        "x0x1x2x3x5x6x7",
        "x0x1x2x4x5x6x7",
        "x0x1x3x4x5x6x7",
        "x0x2x3x4x5x6x7",
        "x1x2x3x4x5x6x7",
    ]

    list_str_exprs = []
    with open("permutations.txt", "r") as txt_file:
        for i in range(4):
            list_str_exprs.append(txt_file.readline())

    list_exprs = [ep.Expr(e) for e in list_str_exprs]
    print(list_exprs)
    
    ctr = 0
    list_grps = []
    for terms in permutations(list_n_1_terms, 4):
        terms = list(terms)
        list_test = []
        for i in range(4):
            list_test.append(list_exprs[i] + terms[i])
        list_grps.append(list_test)
        ctr += 1
        if ctr % 1000 == 0:
            print("Tested {}".format(ctr))
            print(list_grps[100])
            grp_batch = grp.GroupBatch(list_grps)
            if grp_batch.test_permutation().any():
                print("Find!")
                break
            list_grps = []

    if ctr % 1000 != 0:
        print("Tested {}".format(ctr))
        grp_batch = grp.GroupBatch(list_grps)
        if grp_batch.test_permutation().any():
            print("Find!")



if __name__ == "__main__":
    main()