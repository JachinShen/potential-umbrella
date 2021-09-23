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
    with open("cache/permutations_8.txt", "r") as txt_file:
        str_perm = txt_file.read()
    list_str_grps = str_perm.split("\n\n")
    list_grps = [len_t.split("\n") for len_t in list_str_grps]
    list_grps_first_half = [g[:4] for g in list_grps]
    list_grps_second_half = [g[4:] for g in list_grps]
    ctr = 0
    recombined_permutations = []
    for test_grp in product(list_grps_first_half, list_grps_second_half):
        test_grp = test_grp[0] + test_grp[1]
        xor_test_grp = []
        for i in range(8):
            xor_test_grp.append(test_grp[i] + "+x{}".format(i))
        if (grp.Group(test_grp).test_permutation() and
                grp.Group(xor_test_grp).test_permutation()):
            ctr += 1
            recombined_permutations.append("\n".join(test_grp))
            print("Got {} new permutations!".format(ctr))

    print("Got {} new permutations!".format(ctr))
    with open("cache/full_permutations_8.txt", "w") as cache_file:
        for line in recombined_permutations:
            cache_file.write(line)
            cache_file.write("\n\n")


if __name__ == "__main__":
    main()
