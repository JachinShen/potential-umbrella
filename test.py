import expression as ep
one = ep.Expr("one")
zero = ep.Expr("zero")
x0 = ep.Expr("x0")
p, q = zero, zero
print(zero)
print(zero.mat)
print(q)
print(q+one)
print((p+one)*(q+one))
print((p+one)*(q+one)+one)
print(x0*((p+one)*(q+one)+one))
print(x0*((p+one)*(q+one)+one) + (x0+one)*(p+one)*(q+one))