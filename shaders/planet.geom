#version 150 compatibility
#extension GL_EXT_geometry_shader4: enable
#extension GL_ARB_gpu_shader5 : enable

uniform float radiusScale;
uniform float cutoff_x;
uniform float cutoff_y;
uniform float off_size;
uniform float radius_ratio;

flat out float sphere_radius;

void main(void)
{
	
	float halfsize;
	float ratioXPlus = 1.0;
	float ratioXMin = -1.0;
	float ratioY = 1.0;
	float posXMin;
	float posXPlus;
	float posY;
	vec4 pos = gl_PositionIn[0];
	if (pos.x < cutoff_x)
	{
		sphere_radius = radiusScale * gl_FrontColorIn[0].a;
		halfsize = sphere_radius * radius_ratio;
		posXPlus = halfsize;
		posXMin = -halfsize;
		posY = halfsize;
		if ( pos.x + halfsize > cutoff_x )
		{
			ratioXPlus = (cutoff_x - pos.x)/halfsize;
			posXPlus = cutoff_x - pos.x;
		}
		if ( pos.x - halfsize < 0 )
		{
			ratioXMin = (-pos.x)/halfsize;
			posXMin = -pos.x;
		}
		if ( halfsize > cutoff_y/2)
		{
			ratioY = ( cutoff_y/2 )/halfsize;
			posY = cutoff_y/2;
		}
	}
	else
	{
		float index = gl_FrontColorIn[0].b;
		float length = gl_FrontColorIn[0].g;
		halfsize = off_size;
		//pos.y = cutoff_y *( 0.5 - index/length );
		pos.y = cutoff_y * ( 0.5 - index/length );
		pos.x = cutoff_x + off_size * 4;
		posXPlus = halfsize;
		posXMin = -halfsize;
		posY = halfsize;
	}
	vec4 col;
	if ( gl_FrontColorIn[0].r < 1.5)
		col = vec4( 1, 0, 0, 1);
	else if ( gl_FrontColorIn[0].r < 2.5)
		col = vec4( 1, 1, 0, 1);
	else if ( gl_FrontColorIn[0].r < 3.5)
		col = vec4( 1, 0, 1, 1);
	else if ( gl_FrontColorIn[0].r < 4.5)
		col = vec4( 0, 0, 1, 1);
	else if ( gl_FrontColorIn[0].r < 5.5)
		col = vec4( 0, 1, 1, 1);
	else
		col = vec4( 0, 0, 0, 0);
	gl_FrontColor = col;
	gl_TexCoord[0].st = vec2(ratioXPlus,-ratioY);
	gl_Position = pos;
	gl_Position.xy += vec2(posXPlus, -posY);
	gl_Position = gl_ProjectionMatrix* gl_ModelViewMatrix * gl_Position;
	EmitVertex();

	gl_TexCoord[0].st = vec2(ratioXPlus,ratioY);
	gl_Position = pos;
	gl_Position.xy += vec2(posXPlus, posY);
	gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Position;
	EmitVertex();

	gl_TexCoord[0].st = vec2(ratioXMin,-ratioY);
	gl_Position = pos;
	gl_Position.xy += vec2(posXMin, -posY);
	gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Position;
	EmitVertex();

	gl_TexCoord[0].st = vec2(ratioXMin,ratioY);
	gl_Position = pos;
	gl_Position.xy += vec2(posXMin, posY);
	gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Position;
	EmitVertex();

	EndPrimitive();
}