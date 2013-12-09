void main (void)
{
	float x = gl_TexCoord[0].x;
    float y = gl_TexCoord[0].y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )	discard;

    gl_FragColor = gl_Color;
	gl_FragColor.a = sqrt(zz);
	gl_FragDepth = 0.05;
}