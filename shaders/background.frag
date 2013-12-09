varying vec2 var_TexCoord;
uniform float unif_Glow;
uniform vec4 star_color;

uniform float hab_min;
uniform float hab_max;
uniform float orbitScale;
uniform float cutoff_x;
uniform float orbit_ratio;
uniform bool highlight;

void main (void)
{
	float x = var_TexCoord.x;
	float y = var_TexCoord.y;
	float vx = pow(1-x, unif_Glow);
	
	//gl_FragColor.rgb = gl_Color.rgb;
	gl_FragColor.rgb = star_color.rgb;
	//gl_FragColor.rgb = vec3(1.0, 0.0, 0.0);
	gl_FragColor.a = (vx);
	gl_FragDepth = 0.1;
	
	float ratio = orbitScale * orbit_ratio;
	float min = hab_min * ratio / cutoff_x;
	float max = hab_max * ratio / cutoff_x;
	
	if (var_TexCoord.x > min && var_TexCoord.x < max)
	{
		float inter = var_TexCoord.x;
		//gl_FragColor = vec4(0.259, 0.8, 1.0, 0.5);
		gl_FragColor.rgb = vec3(0.259, 0.8, 1.0);
		gl_FragColor.a = 1.0 - abs(inter - (min+max)/2)/(max-min)*2;
	}
	
	if (var_TexCoord.x < 0.005 || var_TexCoord.x > 0.995 || var_TexCoord.y < 0.02 || var_TexCoord.y > 0.98 )
	{
		if (highlight < 1)
			gl_FragColor.rgb = vec3(0,0,0);
		else
			gl_FragColor.rgb = vec3(1,0,0);
		gl_FragColor.a = 1.0;
		gl_FragDepth = 0.01;
	}
}