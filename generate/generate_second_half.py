BASE_CASE = [
    [
    "x0x1+x1x2",
    "x1x2+x2x0",
    "x2x0+x0x1",
    ], [
    "x1x2+x2x0",
    "x2x0+x0x1",
    "x0x1+x1x2",
    ]
]

N = 4
for case in BASE_CASE:
    mapping = {
        "0": "x3x0",
        "1": "x3x1",
        "2": "x3x2",
    }
    split_term = "x0x1x2"
    extend_group = []
    for line in case:
        terms = line.split("+")
        new_terms = [t + "x3" for t in terms]
        extend_group.append(new_terms)
        # new_eq = "+".join(new_terms)
        # print(new_eq)
    # print(new_group)
    for i, line in enumerate(extend_group):
        new_group = []
        for j, line in enumerate(extend_group):
            if j == i:
                split_eq1 = [line[0], split_term]
                split_eq2 = [split_term, line[1]]
                # print(split_eq1, split_eq2)
                new_group.append("+".join(split_eq1))
                new_group.append("+".join(split_eq2))
            else:
                new_group.append("+".join(line))
        print(new_group)

