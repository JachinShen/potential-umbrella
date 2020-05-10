import expression as ep
import group as grp
import itertools


def main():
    names = globals()
    list_x = ["x{}".format(i) for i in range(8)]
    for x in itertools.combinations(list_x, 1):
        x = "".join(x)
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 2):
        x = "".join(x)
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 2):
        x = "".join(x[::-1])
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 3):
        x = "".join(x)
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 3):
        x = "".join(x[::-1])
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 6):
        x = "".join(x)
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 6):
        x = "".join(x[::-1])
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 7):
        x = "".join(x)
        names[x] = ep.Expr(x)
    for x in itertools.combinations(list_x, 7):
        x = "".join(x[::-1])
        names[x] = ep.Expr(x)

    x8 = ep.Expr("x8")
    x9 = ep.Expr("x9")
    x10 = ep.Expr("x10")
    x11 = ep.Expr("x11")
    x12 = ep.Expr("x12")
    x13 = ep.Expr("x13")
    x14 = ep.Expr("x14")
    x15 = ep.Expr("x15")
    one = ep.Expr("one")
    C = ep.Expr("x8x9x10x11x12x13x14x15")
    i, j, k, u, v, w, p = x8, x9, x10, x11, x12, x13, x14

    y0 = (
        x4+x0x1+x0x2+x1x3+x2x3+(x4x5+x6x7)*i+(x4x6+x5x7)*j+(x4x7+x5x6)*k
        + ((x4x5x6+x5x6x7)*p+(x4x5x7+x5x6x7)*(p+one))*(i+j+k+one)
        + ((x4x5x6+x4x6x7)*(p+one)+(x4x5x7+x4x6x7)*p)*(i+j+k)
    )

    y1 = (
        x5+x0x1+x0x2+x1x3+x2x3+(x4x5+x6x7)*i+(x4x6+x5x7)*j+(x4x7+x5x6)*k
        + ((x4x5x7+x4x6x7)*p+(x4x5x6+x4x6x7)*(p+one))*(i+j+k+one)
        + ((x4x5x7+x5x6x7)*(p+one)+(x4x5x6+x5x6x7)*p)*(i+j+k)
    )

    y2 = (
        x6+x0x1+x1x2+x0x3+x2x3+(x4x5+x6x7)*i+(x4x6+x5x7) *
        (j*p+(j+one)*(p+one))+(x4x7+x5x6)*(k*p+(k+one)*(p+one))
        + ((x4x5x7+x5x6x7)*p+(x4x5x7+x4x6x7)*(p+one))*(i+j+k+one)
        + ((x4x5x6+x5x6x7)*(p+one)+(x4x5x6+x4x6x7)*p)*(i+j+k)
    )

    y3 = (
        x7+x0x1+x1x2+x0x3+x2x3+(x4x5+x6x7)*i+(x4x6+x5x7) *
        (j*p+(j+one)*(p+one))+(x4x7+x5x6)*(k*p+(k+one)*(p+one))
        + ((x4x5x6+x4x6x7)*p+(x4x5x6+x5x6x7)*(p+one))*(i+j+k+one)
        + ((x4x5x7+x4x6x7)*(p+one)+(x4x5x7+x5x6x7)*p)*(i+j+k)
    )

    y7 = (
        x3+x7+x7x6+x7x5+x6x4+x5x4+(x3x2+x1x0)*i+(x3x1+x2x0)*j+(x3x0+x2x1)*k
        + ((x3x2x1+x2x1x0)*p+(x3x2x0+x2x1x0)*(p+one))*(i+j+k+one)
        + ((x3x2x1+x3x1x0)*(p+one)+(x3x2x0+x3x1x0)*p)*(i+j+k)
    )

    y6 = (
        x2+x6+x7x6+x7x5+x6x4+x5x4+(x3x2+x1x0)*i+(x3x1+x2x0)*j+(x3x0+x2x1)*k
        + ((x3x2x0+x3x1x0)*p+(x3x2x1+x3x1x0)*(p+one))*(i+j+k+one)
        + ((x3x2x0+x2x1x0)*(p+one)+(x3x2x1+x2x1x0)*p)*(i+j+k)
    )

    y5 = (
        x1+x5+x7x6+x6x5+x7x4+x5x4+(x3x2+x1x0)*i+(x3x1+x2x0) *
        (j*p+(j+one)*(p+one))+(x3x0+x2x1)*(k*p+(k+one)*(p+one))
        + ((x3x2x0+x2x1x0)*p+(x3x2x0+x3x1x0)*(p+one))*(i+j+k+one)
        + ((x3x2x1+x2x1x0)*(p+one)+(x3x2x1+x3x1x0)*p)*(i+j+k)
    )

    y4 = (
        x0+x4+x7x6+x6x5+x7x4+x5x4+(x3x2+x1x0)*i+(x3x1+x2x0) *
        (j*p+(j+one)*(p+one))+(x3x0+x2x1)*(k*p+(k+one)*(p+one))
        + ((x3x2x1+x3x1x0)*p+(x3x2x1+x2x1x0)*(p+one))*(i+j+k+one)
        + ((x3x2x0+x3x1x0)*(p+one)+(x3x2x0+x2x1x0)*p)*(i+j+k)
    )

    """
    y0 = (
        x4+x0x1+x0x2+x1x3+x2x3
        + (x4x5+x6x7)*i + (x4x6+x5x7)*j + (x4x7+x5x6)*k
        + ((x4x5x6+x5x6x7)*p + (x4x6x7+x5x6x7)*(p+one))*(i+j+k+one)
        + ((x4x5x6+x4x5x7)*(p+one)+(x4x5x7+x4x6x7)*p)*(i+j+k)
        + C*x1x2x3x4x5x6 + C*x0x1x2x3x4x5x6
    )

    y1 = (
        x5+x0x2+x1x2+x0x3+x1x3
        + (x4x5+x6x7)*(i*p+(i+one)*(p+one))
        + (x4x6+x5x7)*j
        + (x4x7+x5x6)*(k*p+(k+one)*(p+one))
        + ((x5x6x7+x4x6x7)*p+(x4x5x7+x4x6x7)*(p+one))*(i+j+k+one)
        + ((x4x5x6+x5x6x7)*(p+one)+(x4x5x6+x4x5x7)*p)*(i+j+k)
        + C*x0x1x2x5x6x7+C*x0x1x2x3x4x5x7
    )

    y2 = (
        x6+x0x1+x0x2+x1x3+x2x3
        + (x4x5+x6x7)*i+(x4x6+x5x7)*j+(x4x7+x5x6)*k
        + ((x4x6x7+x4x5x7)*p+(x4x5x6+x4x5x7)*(p+one))*(i+j+k+one)
        + ((x4x6x7+x5x6x7)*(p+one)+(x4x5x6+x5x6x7)*p)*(i+j+k)
        + C*x0x1x3x4x6x7+C*x0x1x2x3x4x6x7
    )

    y3 = (
        x7+x0x2+x1x2+x0x3+x1x3
        + (x4x5+x6x7)*(i*p+(i+one)*(p+one))
        + (x4x6+x5x7)*j
        + (x4x7+x5x6)*(k*p+(k+one)*(p+one))
        + ((x4x5x7+x4x5x6)*p+(x4x5x6+x5x6x7)*(p+one))*(i+j+k+one)
        + ((x4x5x7+x4x6x7)*(p+one)+(x4x6x7+x5x6x7)*p)*(i+j+k)
        + C*x0x2x3x4x5x7+C*x0x1x2x3x5x6x7
    )

    y4 = (
        x0+x4+x7x5+x6x5+x7x4+x6x4
        + (x3x2+x1x0)*(u*p+(u+one)*(p+one))
        + (x3x1+x2x0)*v
        + (x3x0+x2x1)*(w*p+(w+one)*(p+one))
        + ((x3x2x0+x3x2x1)*p+(x3x2x1+x2x1x0)*(p+one))*(u+v+w+one)
        + ((x3x2x0+x3x1x0)*(p+one)+(x3x1x0+x2x1x0)*p)*(u+v+w)
        + C*x7x5x4x3x2x0+C*x7x6x5x4x2x1x0
    )

    y5 = (
        x1+x5+x7x6+x7x5+x6x4+x5x4
        + (x3x2+x1x0)*u+(x3x1+x2x0)*v+(x3x0+x2x1)*w
        + ((x3x1x0+x3x2x0)*p+(x3x2x1+x3x2x0)*(p+one))*(u+v+w+one)
        + ((x3x1x0+x2x1x0)*(p+one)+(x3x2x1+x2x1x0)*p)*(u+v+w)
        + C*x7x6x4x3x1x0+C*x7x6x5x4x3x1x0
    )

    y6 = (
        x2+x6+x7x5+x6x5+x7x4+x6x4
        + (x3x2+x1x0)*(u*p+(u+one)*(p+one))
        + (x3x1+x2x0)*v
        + (x3x0+x2x1)*(w*p+(w+one)*(p+one))
        + ((x2x1x0+x3x1x0)*p+(x3x2x0+x3x1x0)*(p+one))*(u+v+w+one)
        + ((x3x2x1+x2x1x0)*(p+one)+(x3x2x1+x3x2x0)*p)*(u+v+w)
        + C*x7x6x5x2x1x0+C*x7x6x5x4x3x2x0
    )

    y7 = (
        x3+x7+x7x6+x7x5+x6x4+x5x4
        + (x3x2+x1x0)*u + (x3x1+x2x0)*v + (x3x0+x2x1)*w
        + ((x3x2x1+x2x1x0)*p + (x3x1x0+x2x1x0)*(p+one))*(u+v+w+one)
        + ((x3x2x1+x3x2x0)*(p+one)+(x3x2x0+x3x1x0)*p)*(u+v+w)
        + C*x6x5x4x3x2x1 + C*x7x6x5x4x3x2x1
    )
    """

    test_grp = [y0, y1, y2, y3, y4, y5, y6, y7,
                x12, x13, x14, x15, x8+x12, x9+x13, x10+x14, x11+x15]

    test_grp_xor = [y0+x0, y1+x1, y2+x2, y3+x3, y4+x4, y5+x5, y6+x6, y7+x7,
                    x12+x8, x13+x9, x14+x10, x15+x11, x8+x12+x12, x9+x13+x13, x10+x14+x14, x11+x15+x15]

    # test_grp = [x0, x1, x2, x3, x4, x5, x6, x7,
    # x8, x9, x10, x11, x12, x13, x14, x15]
    test_grp = grp.Group(test_grp)
    test_grp_xor = grp.Group(test_grp_xor)
    print(test_grp.test_permutation())
    print(test_grp_xor.test_permutation())


if __name__ == "__main__":
    main()
