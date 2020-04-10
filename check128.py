"""check128.py
"""

from itertools import product
import group as grp


def main():
    """Main"""
    # Appear definitely.
    base_terms = [
        "x4+x0x1+x2x3+x0x2+x1x3",
        "x5+x1x2+x0x3+x0x2+x1x3",
        "x6+x0x1+x2x3+x0x2+x1x3",
        "x7+x1x2+x0x3+x0x2+x1x3",
        "x0+x4+x4x6+x5x6+x4x7+x5x7",
        "x1+x5+x4x5+x4x6+x5x7+x6x7",
        "x2+x6+x4x6+x5x6+x4x7+x5x7",
        "x3+x7+x4x5+x4x6+x5x7+x6x7",
    ]
    grps_128 = []
    for params in product(*[range(2) for i in range(7)]):
        test_grp = []
        for y_i in range(4):
            p, u, v, w, i, j, k = params
            str_expr = base_terms[y_i]
            if y_i % 2 == 1:
                i = (i*p + (i+1)*(p+1)) % 2
                k = (k*p + (k+1)*(p+1)) % 2
            if i == 1:
                str_expr += "+" + "x4x5+x6x7"
            if j == 1:
                str_expr += "+" + "x4x6+x5x7"
            if k == 1:
                str_expr += "+" + "x4x7+x5x6"
            test_grp.append(str_expr)
        for y_i in range(4, 8):
            p, u, v, w, i, j, k = params
            str_expr = base_terms[y_i]
            if y_i % 2 == 0:
                u = (u*p + (u+1)*(p+1)) % 2
                w = (w*p + (w+1)*(p+1)) % 2
            if u == 1:
                str_expr += "+" + "x0x1+x2x3"
            if v == 1:
                str_expr += "+" + "x0x2+x1x3"
            if w == 1:
                str_expr += "+" + "x0x3+x1x2"
            test_grp.append(str_expr)
        p, u, v, w, i, j, k = params
        if (i+j+k+1) % 2 == 1:
            if p == 1:
                test_grp[0] += "+" + "x4x5x6+x5x6x7"
                test_grp[1] += "+" + "x5x6x7+x4x6x7"
                test_grp[2] += "+" + "x4x6x7+x4x5x7"
                test_grp[3] += "+" + "x4x5x7+x4x5x6"
            elif (p+1) % 2 == 1:
                test_grp[0] += "+" + "x4x6x7+x5x6x7"
                test_grp[1] += "+" + "x4x5x7+x4x6x7"
                test_grp[2] += "+" + "x4x5x6+x4x5x7"
                test_grp[3] += "+" + "x4x5x6+x5x6x7"
            else:
                print("Error: p!")
                exit()
        elif (i+j+k) % 2 == 1:
            if (p+1) % 2 == 1:
                test_grp[0] += "+" + "x4x5x6+x4x5x7"
                test_grp[1] += "+" + "x4x5x6+x5x6x7"
                test_grp[2] += "+" + "x4x6x7+x5x6x7"
                test_grp[3] += "+" + "x4x5x7+x4x6x7"
            elif p == 1:
                test_grp[0] += "+" + "x4x5x7+x4x6x7"
                test_grp[1] += "+" + "x4x5x6+x4x5x7"
                test_grp[2] += "+" + "x4x5x6+x5x6x7"
                test_grp[3] += "+" + "x4x6x7+x5x6x7"
            else:
                print("Error: p!")
                exit()
        if (u+v+w+1) % 2 == 1:
            if p == 1:
                test_grp[4] += "+" + "x0x2x3+x1x2x3"
                test_grp[5] += "+" + "x0x1x3+x0x2x3"
                test_grp[6] += "+" + "x0x1x2+x0x1x3"
                test_grp[7] += "+" + "x0x1x2+x1x2x3"
            elif (p+1) % 2 == 1:
                test_grp[4] += "+" + "x0x1x2+x1x2x3"
                test_grp[5] += "+" + "x0x2x3+x1x2x3"
                test_grp[6] += "+" + "x0x1x3+x0x2x3"
                test_grp[7] += "+" + "x0x1x2+x0x1x3"
            else:
                print("Error: p!")
                exit()
        elif (u+v+w) % 2 == 1:
            if (p+1) % 2 == 1:
                test_grp[4] += "+" + "x0x1x3+x0x2x3"
                test_grp[5] += "+" + "x0x1x2+x0x1x3"
                test_grp[6] += "+" + "x0x1x2+x1x2x3"
                test_grp[7] += "+" + "x0x2x3+x1x2x3"
            elif p == 1:
                test_grp[4] += "+" + "x0x1x2+x0x1x3"
                test_grp[5] += "+" + "x0x1x2+x1x2x3"
                test_grp[6] += "+" + "x0x2x3+x1x2x3"
                test_grp[7] += "+" + "x0x1x3+x0x2x3"
            else:
                print("Error: p!")
                exit()
        xor_test_grp = []
        for i in range(8):
            xor_test_grp.append(test_grp[i] + "+x{}".format(i))
        if (grp.Group(test_grp).test_permutation() and
                grp.Group(xor_test_grp).test_permutation()):
            print("True")
        else:
            print("False")
        grps_128.append("\n".join(test_grp))
    with open("half_permutations2.txt", "w") as f:
        f.write("\n\n".join(grps_128))


if __name__ == "__main__":
    main()
