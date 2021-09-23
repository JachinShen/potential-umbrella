"""cache_expression.py

Cache balance expressions for later selection.
Balance is necessary to permutation.
"""

from itertools import combinations, permutations, product, chain
import expression as ep


def main():
    """Main"""
    # Candidates.
    deg_n1 = ["".join(t) for t in combinations(["x{}".format(i) for i in range(6,12)], 5)]
    print(deg_n1)

    deg_n2 = ["".join(t) for t in combinations(["x{}".format(i) for i in range(6,12)], 3)]
    deg_n2 = ["+".join((i, j)) for i, j in zip(deg_n2, deg_n2[::-1])][:10]
    # deg_n2 = [
    #     "x6x7+x8x9+x10x11",
    #     "x6x9+x7x10+x8x11",
    #     # "x6x8+x7x11+x9x10",
    #     # "x6x10+x9x11+x7x8",
    #     # "x6x11+x8x10+x7x9",
    # ]
    print(deg_n2)

    # deg_n2_0 = [
    #     "x0x1+x2x3+x4x5",
    #     "x0x3+x1x4+x2x5",
    #     # "x0x2+x1x5+x3x4",
    #     # "x0x4+x3x5+x1x2",
    #     # "x0x5+x2x4+x1x3",
    # ]
    deg_n2_0 = ["".join(t) for t in combinations(["x{}".format(i) for i in range(0,6)], 3)]
    deg_n2_0 = ["+".join((i, j)) for i, j in zip(deg_n2_0, deg_n2_0[::-1])][:10]
    # deg_n2_0 = ["+".join(t) for t in combinations(deg_n2_0, 2)]
    print(deg_n2_0)

    cand_terms = [
        (deg_n2, 2),
        (deg_n2_0, 2),
        (deg_n1, 2)
    ]
    cached_exprs_grp = []
    # Appear definitely.
    base_terms = [
        # "x4+x0x1+x0x2+x1x3+x2x3",
        # "x5+x0x2+x1x2+x0x3+x1x3",
        # "x6+x0x1+x0x2+x1x3+x2x3",
        # "x7+x0x2+x1x2+x0x3+x1x3",
        # "x4+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        # "x5+x5x6+x4x7",
        # "x6+x5x6+x4x7",
        # "x7+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        "x6", "x7", "x8", "x9", "x10", "x11"
    ]
    # Find balance candidates for every expression.
    for b_term in base_terms:
        cand_exprs = []
        for terms in product(*[combinations(t, n) for t, n in cand_terms]):
            terms = list(map(list, terms))
            terms = list(chain.from_iterable(terms))
            str_expr = "+".join(list(terms) + [b_term])
            expr = ep.Expr(str_expr)
            if expr.test_balance():
                cand_exprs.append(str_expr)
        cached_exprs_grp.append("|".join(cand_exprs))
        cnt = len(cand_exprs)
        print("Candidates: ", cnt)
    # Use txt for convenience of reading.
    with open("cache/cached_balance_expression.txt", "w") as cache_file:
        for line in cached_exprs_grp:
            cache_file.write(line)
            cache_file.write("\n")


if __name__ == "__main__":
    main()
