varying vec2 var_TexCoord;
varying vec3 var_Normal;
varying vec3 var_EyeVector;

uniform vec4 star_color;

void main(void)
{
	gl_Position = ftransform();
	vec4 eyeSpacePosition = gl_ModelViewMatrix * gl_Vertex;
	
	var_TexCoord = gl_Color.rg;
	
	var_EyeVector = -eyeSpacePosition.xyz;
	var_Normal = gl_NormalMatrix * gl_Normal;
	
	gl_FrontColor = vec4(1,0,0,1);
	//gl_FrontColor = gl_Color;
}