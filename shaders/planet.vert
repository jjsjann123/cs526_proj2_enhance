uniform float orbitScale;
uniform float orbit_ratio;

uniform float cutoff_x;

void main(void)
{
	vec4 pos = gl_Vertex;
	float ratio = orbitScale * orbit_ratio;
	//pos.x = pos.x * orbitScale;
	pos.x = pos.x * ratio;
	gl_Position = pos;
	gl_FrontColor = gl_Color;
}