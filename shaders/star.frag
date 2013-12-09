#version 150 compatibility
#extension GL_ARB_gpu_shader5 : enable

flat in float sphere_radius;

void main (void)
{
    float x = gl_TexCoord[0].x;
    float y = gl_TexCoord[0].y;
    float zz = 1.0 - x*x - y*y;

    if (zz <= 0.0 )	discard;

	float q = pow(zz, 16);
	if ( q < 0.01 )
		discard;
	//gl_FragColor.a = pow(zz, 16);
	gl_FragColor = gl_Color;
	gl_FragColor.a = q;
}
