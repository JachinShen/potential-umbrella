
void forward(
    int x0, int x1, int x2, int x3, int x4, int x5, int x6, int x7, int x8, int x9, int x10, int x11,
    int* y0, int* y1, int* y2, int* y3, int* y4, int* y5, int* y6, int* y7, int* y8, int* y9, int* y10, int* y11) {
	*y0 = x6+x0*x1+x0*x2+x0*x3+x0*x4+x1*x5+x2*x5+x3*x5+x4*x5+x6*x7*x8*x9*x10+x7*x8*x9*x10*x11+x1*x2*x3*x4*x5*x6*x7*x8*x9*x10+x0*x1*x2*x3*x4*x5*x6*x7*x8*x9*x10;
	*y1 = x7+x0*x1+x1*x2+x1*x3+x0*x4+x2*x4+x3*x4+x1*x5+x4*x5+x6*x7*x8*x9*x11+x6*x8*x9*x10*x11+x0*x2*x3*x4*x5*x6*x7*x8*x9*x11+x0*x1*x2*x3*x4*x5*x6*x7*x8*x9*x11;
	*y2 = x8+x0*x2+x1*x2+x0*x3+x1*x3+x2*x4+x3*x4+x2*x5+x3*x5+x6*x7*x8*x10*x11+x6*x7*x9*x10*x11+x0*x1*x3*x4*x5*x6*x7*x8*x10*x11+x0*x1*x2*x3*x4*x5*x6*x7*x8*x10*x11;
	*y3 = x9+x0*x2+x1*x2+x0*x3+x1*x3+x2*x4+x3*x4+x2*x5+x3*x5+x6*x7*x8*x10*x11+x6*x7*x9*x10*x11+x0*x1*x2*x4*x5*x6*x7*x9*x10*x11+x0*x1*x2*x3*x4*x5*x6*x7*x9*x10*x11;
	*y4 = x10+x0*x1+x1*x2+x1*x3+x0*x4+x2*x4+x3*x4+x1*x5+x4*x5+x6*x7*x8*x9*x11+x6*x8*x9*x10*x11+x0*x1*x2*x3*x5*x6*x8*x9*x10*x11+x0*x1*x2*x3*x4*x5*x6*x8*x9*x10*x11;
	*y5 = x11+x0*x1+x0*x2+x0*x3+x0*x4+x1*x5+x2*x5+x3*x5+x4*x5+x6*x7*x8*x9*x10+x7*x8*x9*x10*x11+x0*x1*x2*x3*x4*x7*x8*x9*x10*x11+x0*x1*x2*x3*x4*x5*x7*x8*x9*x10*x11;
	*y6 = x0+x6+x6*x7+x6*x8+x6*x9+x6*x10+x7*x11+x8*x11+x9*x11+x10*x11+x0*x1*x2*x3*x4+x1*x2*x3*x4*x5+x0*x1*x2*x3*x4*x7*x8*x9*x10*x11+x0*x1*x2*x3*x4*x6*x7*x8*x9*x10*x11;
	*y7 = x1+x7+x6*x7+x7*x8+x7*x9+x6*x10+x8*x10+x9*x10+x7*x11+x10*x11+x0*x1*x2*x3*x5+x0*x2*x3*x4*x5+x0*x1*x2*x3*x5*x6*x8*x9*x10*x11+x0*x1*x2*x3*x5*x6*x7*x8*x9*x10*x11;
	*y8 = x2+x8+x6*x8+x7*x8+x6*x9+x7*x9+x8*x10+x9*x10+x8*x11+x9*x11+x0*x1*x2*x4*x5+x0*x1*x3*x4*x5+x0*x1*x2*x4*x5*x6*x7*x9*x10*x11+x0*x1*x2*x4*x5*x6*x7*x8*x9*x10*x11;
	*y9 = x3+x9+x6*x8+x7*x8+x6*x9+x7*x9+x8*x10+x9*x10+x8*x11+x9*x11+x0*x1*x2*x4*x5+x0*x1*x3*x4*x5+x0*x1*x3*x4*x5*x6*x7*x8*x10*x11+x0*x1*x3*x4*x5*x6*x7*x8*x9*x10*x11;
	*y10 = x4+x10+x6*x7+x7*x8+x7*x9+x6*x10+x8*x10+x9*x10+x7*x11+x10*x11+x0*x1*x2*x3*x5+x0*x2*x3*x4*x5+x0*x2*x3*x4*x5*x6*x7*x8*x9*x11+x0*x2*x3*x4*x5*x6*x7*x8*x9*x10*x11;
	*y11 = x5+x11+x6*x7+x6*x8+x6*x9+x6*x10+x7*x11+x8*x11+x9*x11+x10*x11+x0*x1*x2*x3*x4+x1*x2*x3*x4*x5+x1*x2*x3*x4*x5*x6*x7*x8*x9*x10+x1*x2*x3*x4*x5*x6*x7*x8*x9*x10*x11;
}
    