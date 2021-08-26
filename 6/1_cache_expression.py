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
        # (ep.TERMS_FIRST_HALF[0], 2),
        (ep.TERMS_SECOND_HALF[0], 2),
        # (ep.TERMS[2], 2),
    ]
    cached_exprs_grp = []
    # Appear definitely.
    base_terms = ep.TERMS[0][ep.N_X//2:]
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
