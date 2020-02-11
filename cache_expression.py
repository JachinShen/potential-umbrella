"""cache_expression.py

Cache balance expressions for later selection.
Balance is necessary to permutation.
"""

from itertools import permutations, combinations, product, chain
import expression as ep


def main():
    """Main"""
    # Appear definitely.
    base_terms = [
        "x4+x4x5x6+x5x6x7",
        "x5+x5x6x7+x6x7x4",
        "x6+x6x7x4+x7x4x5",
        "x7+x7x4x5+x4x5x6",
    ]
    # Candidates.
    cand_terms_1 = [
        "x0x1x2x3x4x5x6",
        "x0x1x2x3x4x5x7",
        "x0x1x2x3x4x6x7",
        "x0x1x2x3x5x6x7",
        "x0x1x2x4x5x6x7",
        "x0x1x3x4x5x6x7",
        "x0x2x3x4x5x6x7",
        "x1x2x3x4x5x6x7",
    ]
    cand_terms_2 = [
        "x1x2x3x4x5x6",
        "x0x2x3x4x5x7",
        "x0x1x3x4x6x7",
        "x0x1x2x5x6x7",
        #"x4x5", "x4x6", "x4x7", "x5x6", "x5x7", "x6x7",
        #"x4x5x6", "x5x6x7", "x6x7x4", "x7x4x5",
    ]
    cached_exprs_grp = []
    cnt = 0
    # Find balance candidates for every expression.
    for b_term in base_terms:
        cand_exprs = []
        for terms in product(combinations(cand_terms_1, 1), combinations(cand_terms_2, 1)):
            terms = list(map(list, terms))
            terms = list(chain.from_iterable(terms))
            str_expr = "+".join(list(terms) + [b_term])
            expr = ep.Expr(str_expr)
            if expr.test_balance():
                cand_exprs.append(str_expr)
                cnt += 1
        cached_exprs_grp.append("|".join(cand_exprs))
    # Use txt for convenience of reading.
    with open("cached_balance_expression.txt", "w") as cache_file:
        for line in cached_exprs_grp:
            cache_file.write(line)
            cache_file.write("\n")
    print("Candidates: ", cnt)


if __name__ == "__main__":
    main()
