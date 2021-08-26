"""cache_expression.py

Cache balance expressions for later selection.
Balance is necessary to permutation.
"""

from itertools import combinations, product, chain
import expression as ep


def main():
    """Main"""
    # Candidates.
    cand_terms = [
        # (["x4x5x6", "x5x6x7", "x6x7x4", "x7x4x5"], 2),
        # (["x0x1+x2x3", "zero"], 1),
        # (["x0x2+x1x3", "zero"], 1),
        # (["x1x2+x0x3", "zero"], 1),
        # (["x4x5+x4x6+x5x7+x6x7", "x4x5+x5x6+x4x7+x6x7",
        #  "x4x6+x5x6+x4x7+x5x7", "x4x5+x4x6+x5x6+x4x7+x5x7+x6x7"], 1),
        # (["x0x1+x0x2+x1x3+x2x3", "x0x1+x1x2+x0x3+x2x3", "x0x2+x1x2+x0x3+x1x3"], 1),
        # (["x0x1+x0x2+x1x3+x2x3"], 1),
        # (["x0x1+x2x3", "x0x2+x1x3", "x1x2+x0x3"], 1),
        ([
            "x0x1+x2x3", "x0x1+x2x4", "x0x1+x3x4", 
            "x0x2+x1x3", "x0x2+x1x4", "x0x2+x3x4",
            "x0x3+x1x2", "x0x3+x1x4", "x0x3+x2x4",
            "x0x4+x1x2", "x0x4+x1x3", "x0x4+x2x3",
            "x1x2+x3x4",
        ], 2)

        # (["x4x5+x6x7", "zero"], 1),
        # (["x4x6+x5x7", "zero"], 1),
        # (["x5x6+x4x7", "zero"], 1),
        # (["x4x5+x6x7", "x4x6+x5x7", "x5x6+x4x7"], 1),
        # (["x4x5+x4x6+x5x7+x6x7", "x4x5+x5x6+x4x7+x6x7", "x4x6+x5x6+x4x7+x5x7"], 1),
        # ([
        #     "x5x6+x7x8", "x5x6+x7x9", "x5x6+x8x9", 
        #     "x5x7+x6x8", "x5x7+x6x9", "x5x7+x8x9",
        #     "x5x8+x6x7", "x5x8+x6x9", "x5x8+x7x9",
        #     "x5x9+x6x7", "x5x9+x6x8", "x5x9+x7x8"
        # ], 2)
    ]
    cached_exprs_grp = []
    # Appear definitely.
    base_terms = [
        # "x4", "x5", "x6", "x7"
        # "x4+x0x1+x0x2+x1x3+x2x3",
        # "x5+x0x2+x1x2+x0x3+x1x3",
        # "x6+x0x1+x0x2+x1x3+x2x3",
        # "x7+x0x2+x1x2+x0x3+x1x3",
        # "x4+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        # "x5+x5x6+x4x7",
        # "x6+x5x6+x4x7",
        # "x7+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        # "x4+x4x5x6+x4x6x7+x1x2x3x4x5x6+x0x1x2x3x4x5x6",
        # "x5+x4x5x7+x5x6x7+x0x2x3x4x5x7+x0x1x2x3x4x5x7",
        # "x6+x4x5x6+x5x6x7+x0x1x3x4x6x7+x0x1x2x3x4x6x7",
        # "x7+x4x5x7+x4x6x7+x0x1x2x5x6x7+x0x1x2x3x5x6x7",
        # "x4+x4x5x6+x4x6x7",
        # "x5+x4x5x7+x5x6x7",
        # "x6+x4x5x6+x5x6x7",
        # "x7+x4x5x7+x4x6x7",
        # "x4+x4x5x6+x4x5x7",
        # "x5+x4x5x6+x5x6x7",
        # "x6+x4x6x7+x5x6x7",
        # "x7+x4x5x7+x4x6x7"
        # "x4+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        # "x5+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        # "x6+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        # "x7+x4x5+x4x6+x5x6+x4x7+x5x7+x6x7",
        'x5+x5x6x7x8+x6x7x8x9',
        'x6+x6x7x8x9+x7x8x9x5',
        'x7+x7x8x9x5+x8x9x5x6',
        "x8+x8x9x5x6+x9x5x6x7",
        "x9+x9x5x6x7+x5x6x7x8"
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
    with open("cache/cached_balance_expression_8.txt", "w") as cache_file:
        for line in cached_exprs_grp:
            cache_file.write(line)
            cache_file.write("\n")


if __name__ == "__main__":
    main()
