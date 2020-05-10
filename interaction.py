"""interaction.py
"""

import numpy as np

import expression as ep
import group as grp
import utils


def main():
    """Main
    """
    print(
        "1: test balance of expression. \n"
        "2: test permutation of group. \n"
        "3: generate n-degree terms. \n"
        "4: expand product. \n"
    )

    cmd = input()
    if cmd == "1":
        test_balance()
    elif cmd == "2":
        test_permutation()
    elif cmd == "3":
        generate_terms()
    elif cmd == "4":
        expand_product()
    else:
        print("Unknown command! Exit!")


def test_permutation():
    """Test permutation
    """
    while True:
        list_str_exprs = []
        for i in range(ep.N_X):
            print("Please input expression {}:".format(i+1))
            str_expr = input()
            if str_expr == "q":
                print("Exit")
                break
            list_str_exprs.append(str_expr)
        group = grp.Group(list_str_exprs)
        if group.test_permutation():
            print("Permutation!")
        else:
            print("Not permutation!")


def test_balance():
    """Test balance
    """
    while True:
        print("Please input expression:")
        str_expr = input()
        if str_expr == "q":
            print("Exit")
            break
        expr = ep.Expr(str_expr)
        if expr.test_balance():
            print("Balance!")
        else:
            print("Imbalance!")


def generate_terms():
    """Generate n-degree terms
    """
    all_terms = np.zeros([2**(ep.N_X//2), ep.LEN_ALPHA], dtype=np.bool)
    all_terms[:, 0] = False
    all_terms[:, ep.N_X//2+1:-1] = utils.get_all_unpacked_bits(ep.N_X//2)
    all_terms[:, -1] = True
    deg_terms = all_terms.sum(axis=1) - 1
    while True:
        print("Please input the degree:")
        deg = int(input())
        mask = (deg_terms == deg)
        expr = ep.Expr(mat=all_terms[mask])
        print(expr)


def expand_product():
    while True:
        print("Please input expression1:")
        expr1 = ep.Expr(input())
        print("Please input expression2:")
        expr2 = ep.Expr(input())
        print("Product: ", expr1*expr2)


if __name__ == "__main__":
    main()
