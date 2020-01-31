"""
Step 1: Cache balance expressions
"""
from itertools import permutations
from expression import Expression

def main():
    """
    Main
    """
    base_terms = [
        "x4",
        "x5",
        "x6",
        "x7",
    ]
    cand_terms = ["x4x5", "x4x6", "x4x7", "x5x6", "x5x7", "x6x7"]
    cached_exprs_grp = []
    cnt = 0
    for b_term in base_terms:
        cand_exprs = []
        for terms in permutations(cand_terms, 3):
            str_expr = "+".join(list(terms) + [b_term])
            expr = Expression(str_expr)
            if expr.test_balance():
                cand_exprs.append(str_expr)
                cnt += 1
        """
        for i, term_i in enumerate(cand_terms):
            for j, term_j in enumerate(cand_terms[i+1:]):
        """
        cached_exprs_grp.append("|".join(cand_exprs))
    with open("cached_balance_expression.txt", "w") as cache_file:
        for line in cached_exprs_grp:
            cache_file.write(line)
            cache_file.write("\n")
    print("Candidates: ", cnt)

if __name__ == "__main__":
    main()
