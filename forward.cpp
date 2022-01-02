     void forward( 
     int x0, int x1, int x2, int x3, int x4, int x5, int x6, int x7, 
     int y0, int y1, int y2, int y3, int y4, int y5, int y6, int y7) { 
     	y0 = x4+x0x2+x1x2+x0x3+x1x3+x4x6x7+x5x6x7+x0x1x3x4x6x7+x0x1x2x3x4x5x6;
	y1 = x5+x0x2+x1x2+x0x3+x1x3+x4x6x7+x5x6x7+x0x1x2x5x6x7+x0x1x2x3x4x5x7;
	y2 = x6+x0x2+x1x2+x0x3+x1x3+x4x5x6+x4x5x7+x1x2x3x4x5x6+x0x1x2x3x4x6x7;
	y3 = x7+x0x2+x1x2+x0x3+x1x3+x4x5x6+x4x5x7+x0x2x3x4x5x7+x0x1x2x3x5x6x7;
	y4 = x0+x4+x4x6+x5x6+x4x7+x5x7+x0x2x3+x1x2x3+x0x2x3x4x5x7+x0x1x2x4x5x6x7;
	y5 = x1+x5+x4x6+x5x6+x4x7+x5x7+x0x2x3+x1x2x3+x1x2x3x4x5x6+x0x1x3x4x5x6x7;
	y6 = x2+x6+x4x6+x5x6+x4x7+x5x7+x0x1x2+x0x1x3+x0x1x2x5x6x7+x0x2x3x4x5x6x7;
	y7 = x3+x7+x4x6+x5x6+x4x7+x5x7+x0x1x2+x0x1x3+x0x1x3x4x6x7+x1x2x3x4x5x6x7;
     }
     