double inverse(double y[]) {
  double y0 = y[0];
  double y1 = y[1];
  double y2 = y[2];
  double y3 = y[3];
  double y4 = y[4];
  double y5 = y[5];
  double y6 = y[6];
  double y7 = y[7];
  double x0 =
      y0 + y4 + y1 * y4 + y2 * y5 + y3 * y6 + y5 * y6 + y0 * y7 + y4 * y7 +
      y0 * y1 * y4 + y0 * y2 * y4 + y1 * y2 * y5 + y1 * y4 * y5 + y2 * y4 * y5 +
      y3 * y4 * y5 + y0 * y2 * y6 + y1 * y2 * y6 + y0 * y3 * y6 + y2 * y3 * y6 +
      y1 * y4 * y6 + y3 * y4 * y6 + y0 * y5 * y6 + y1 * y5 * y6 + y3 * y5 * y6 +
      y4 * y5 * y6 + y0 * y2 * y7 + y0 * y3 * y7 + y1 * y3 * y7 + y1 * y4 * y7 +
      y2 * y4 * y7 + y3 * y4 * y7 + y0 * y6 * y7 + y1 * y6 * y7 + y3 * y6 * y7 +
      y4 * y6 * y7 + y0 * y1 * y3 * y4 + y0 * y2 * y3 * y4 + y0 * y1 * y3 * y5 +
      y0 * y2 * y3 * y5 + y0 * y1 * y4 * y5 + y2 * y3 * y4 * y5 +
      y0 * y1 * y3 * y6 + y0 * y2 * y3 * y6 + y0 * y2 * y4 * y6 +
      y1 * y2 * y4 * y6 + y0 * y3 * y4 * y6 + y1 * y3 * y4 * y6 +
      y0 * y1 * y5 * y6 + y0 * y2 * y5 * y6 + y1 * y2 * y5 * y6 +
      y0 * y3 * y5 * y6 + y1 * y3 * y5 * y6 + y2 * y3 * y5 * y6 +
      y0 * y1 * y3 * y7 + y0 * y1 * y4 * y7 + y2 * y3 * y4 * y7 +
      y0 * y1 * y6 * y7 + y0 * y2 * y6 * y7 + y1 * y2 * y6 * y7 +
      y0 * y3 * y6 * y7 + y1 * y3 * y6 * y7 + y2 * y3 * y6 * y7 +
      y0 * y1 * y2 * y4 * y5 + y0 * y2 * y3 * y4 * y5 + y0 * y1 * y2 * y3 * y6 +
      y0 * y1 * y2 * y5 * y6 + y0 * y2 * y3 * y5 * y6 + y0 * y1 * y2 * y4 * y7 +
      y0 * y2 * y3 * y5 * y7 + y0 * y1 * y2 * y6 * y7 + y0 * y2 * y3 * y6 * y7 +
      y0 * y1 * y2 * y3 * y4 * y6 + y0 * y1 * y2 * y3 * y5 * y6 +
      y0 * y2 * y3 * y4 * y5 * y7 + y0 * y1 * y2 * y3 * y4 * y5 * y6;
  return x0;
}