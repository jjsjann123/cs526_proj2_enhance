varying vec2 var_TexCoord;

uniform float ratio;

void main (void)
{
	float x = var_TexCoord.x-0.5;
	float y = var_TexCoord.y-0.5;
	x = x*2;
	y = y*2;
	float z = x*x + y*y;
	
	if ( z > 1 )
	{
		discard;
	}
	float q = sqrt(z);
	if ( q < ratio )
	{
		discard;
	}
	gl_FragColor.rgb = gl_Color.rgb;
	gl_FragColor.a = 1.0 - abs(q - (1+ratio)/2)/(1-ratio)*2;
}