"""check256.py
"""

from itertools import product
import group as grp


def main_256_128():
    """Main
    """
    with open("permutations3.txt", "r") as txt_file:
        str_perm = txt_file.read()
    list_str_grps = str_perm.split("\n\n")
    list_grps = [len_t.split("\n") for len_t in list_str_grps]
    list_grps_part1 = list_grps[:4] + list_grps[-4:]
    list_grps_part2 = list_grps[4:-4]
    list_grps_first_half = [g[:4] for g in list_grps_part1]
    list_grps_second_half = [g[4:] for g in list_grps_part1]
    ctr = 0
    for test_grp in product(list_grps_first_half, list_grps_second_half):
        test_grp = test_grp[0] + test_grp[1]
        xor_test_grp = []
        for i in range(8):
            xor_test_grp.append(test_grp[i] + "+x{}".format(i))
        ctr += 1
        if (grp.Group(test_grp).test_permutation() and
                grp.Group(xor_test_grp).test_permutation()):
            print("{}: Y".format(ctr))
        else:
            print("{}: N".format(ctr))

    list_grps_first_half = [g[:4] for g in list_grps_part2]
    list_grps_second_half = [g[4:] for g in list_grps_part2]
    ctr = 0
    for test_grp in product(list_grps_first_half, list_grps_second_half):
        test_grp = test_grp[0] + test_grp[1]
        xor_test_grp = []
        for i in range(8):
            xor_test_grp.append(test_grp[i] + "+x{}".format(i))
        ctr += 1
        if (grp.Group(test_grp).test_permutation() and
                grp.Group(xor_test_grp).test_permutation()):
            print("{}: Y".format(ctr))
        else:
            print("{}: N".format(ctr))


def main():
    """Main
    """
    with open("permutations3.txt", "r") as txt_file:
        str_perm = txt_file.read()
    list_str_grps = str_perm.split("\n\n")
    list_grps = [len_t.split("\n") for len_t in list_str_grps]
    list_grps_first_half = [g[:4] for g in list_grps]
    list_grps_second_half = [g[4:] for g in list_grps]
    ctr = 0
    for test_grp in product(list_grps_first_half, list_grps_second_half):
        test_grp = test_grp[0] + test_grp[1]
        xor_test_grp = []
        for i in range(8):
            xor_test_grp.append(test_grp[i] + "+x{}".format(i))
        if (grp.Group(test_grp).test_permutation() and
                grp.Group(xor_test_grp).test_permutation()):
            ctr += 1
            print("{}: Y".format(ctr))
        else:
            pass
            print("{}: N".format(ctr))


if __name__ == "__main__":
    main()
