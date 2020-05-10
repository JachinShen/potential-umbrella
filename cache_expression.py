"""cache_expression.py

Cache balance expressions for later selection.
Balance is necessary to permutation.
"""

from itertools import combinations, product, chain
import expression as ep


def main():
    """Main"""
    # Appear definitely.
    """
    base_terms = ["x{}".format(i) for i in range(ep.N_X//2, ep.N_X)]
    """
    base_terms = [
        # "x4+x0x1+x2x3+x0x2+x1x3+x4x5x6+x5x6x7",
        # "x5+x1x2+x0x3+x0x2+x1x3+x5x6x7+x6x7x4",
        # "x6+x0x1+x2x3+x0x2+x1x3+x6x7x4+x7x4x5",
        # "x7+x1x2+x0x3+x0x2+x1x3+x7x4x5+x4x5x6",
        # "x4+x0x1+x2x3+x0x2+x1x3",
        # "x5+x1x2+x0x3+x0x2+x1x3",
        # "x6+x0x1+x2x3+x0x2+x1x3",
        # "x7+x1x2+x0x3+x0x2+x1x3",
        "x4+x0x1+x0x2+x1x3+x2x3",
        "x5+x0x1+x0x2+x1x3+x2x3",
        "x6+x0x1+x1x2+x0x3+x2x3",
        "x7+x0x1+x1x2+x0x3+x2x3",
        # "x4+x0x1+x0x2+x1x3+x2x3",
        # "x5+x0x2+x1x2+x0x3+x1x3",
        # "x6+x0x1+x0x2+x1x3+x2x3",
        # "x7+x0x2+x1x2+x0x3+x1x3",
    ]
    # Candidates.
    cand_terms = [
        ([
            "x0x1", "x0x2", "x0x3", "x1x2", "x1x3", "x2x3",
        ], 0),
        ([
            "x4x5", "x4x6", "x4x7", "x5x6", "x5x7", "x6x7"
        ], 0),
        ([
            "x4x5", "x4x6", "x4x7", "x5x6", "x5x7", "x6x7"
        ], 0),
        ([
            "x4", "x5", "x6", "x7"
        ], 0),
        ([
            "x4x5x6", "x5x6x7", "x6x7x4", "x7x4x5",
        ], 2),
        ([
            "x0x1+x2x3", "zero"
        ], 0),
        ([
            "x0x2+x1x3", "zero"
        ], 0),
        ([
            "x1x2+x0x3", "zero"
        ], 0),
        ([
            "x4x5+x6x7", "zero"
        ], 1),
        ([
            "x4x6+x5x7", "zero"
        ], 1),
        ([
            "x5x6+x4x7", "zero"
        ], 1),
    ]
    cached_exprs_grp = []
    # Find balance candidates for every expression.
    for b_term in base_terms:
        cand_exprs = []
        for terms in product(*[combinations(t, n) for t, n in cand_terms]):
            terms = list(map(list, terms))
            terms = list(chain.from_iterable(terms))
            str_expr = "+".join(list(terms) + [b_term])
            expr = ep.Expr(str_expr)
            if expr.test_balance() and expr.n_terms >= 7 + 1:
                cand_exprs.append(str_expr)
        cached_exprs_grp.append("|".join(cand_exprs))
        cnt = len(cand_exprs)
    # Use txt for convenience of reading.
    with open("cached_balance_expression.txt", "w") as cache_file:
        for line in cached_exprs_grp:
            cache_file.write(line)
            cache_file.write("\n")
    print("Candidates: ", cnt)


if __name__ == "__main__":
    main()
