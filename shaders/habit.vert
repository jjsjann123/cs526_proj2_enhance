varying vec2 var_TexCoord;

void main(void)
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	
	var_TexCoord = gl_MultiTexCoord0.xy;
	gl_FrontColor = gl_Color;
}