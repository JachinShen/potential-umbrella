"""interaction.py
"""

import expression as ep
import group as grp

def main():
    """Main
    """
    print(
        "1: test balance of expression. \n"
        "2: test permutation of group. \n"
    )

    cmd = input()
    if cmd == "1":
        test_balance()
    elif cmd == "2":
        test_permutation()
    else:
        print("Unknown command! Exit!")

def test_permutation():
    """Test permutation
    """
    while True:
        list_str_exprs = []
        for i in range(ep.N_X//2):
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

if __name__ == "__main__":
    main()
