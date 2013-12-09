from omega import *
from omegaToolkit import *
from cyclops import *
from math import *
from euclid import *
from fun import *



def buildGalaxy(systems):
	global stellarColorMap
	global galaxyScale
	global fontSize
	galaxyModel = ModelGeometry.create('galaxyModel')
	for systemName in systems:
		stellar = systems[systemName]['stellar']
		star = systems[systemName]['star']
		distance = stellar['distance']
		alpha = stellar['rightascension']
		beta = stellar['declination']
		x = distance * cos(beta) * cos(alpha)
		y = distance * sin(beta)
		z = distance * cos(beta) * sin(alpha)
		galaxyModel.addVertex ( Vector3(x, y, z))
		t = Text3D.create( 'fonts/arial.ttf', fontSize, stellar['name'] )
		t.setPosition(Vector3(x, y, z))
		t.setFixedSize(True)
		t.setFontResolution(120)
		t.setFacingCamera(getDefaultCamera())
		galaxy.addChild(t)
		
		rgb = stellarMap[star[0]['spectraltype']]
		
		galaxyModel.addColor ( Color( rgb[0], rgb[1], rgb[2], star[0]['radius']) )
	galaxyModel.addPrimitive(PrimitiveType.Points, 0, len(systems))
	getSceneManager().addModel(galaxyModel)
	
	starProgram = ProgramAsset()
	starProgram.name = "stars"
	starDir = './shaders/'
	starProgram.vertexShaderName = starDir + "star.vert"
	starProgram.fragmentShaderName = starDir + "star.frag"
	starProgram.geometryShaderName = starDir + "star.geom"
	starProgram.geometryOutVertices = 4
	starProgram.geometryInput = PrimitiveType.Points
	starProgram.geometryOutput = PrimitiveType.TriangleStrip
	getSceneManager().addProgram(starProgram)
	
	galaxyCore = StaticObject.create('galaxyModel')
	inst = galaxyCore
	inst.setPosition(Vector3(0,0,0))
	inst.getMaterial().setProgram('stars')
	inst.getMaterial().setTransparent(True)
	inst.getMaterial().setAdditive(True)
	inst.getMaterial().setDepthTestEnabled(True)
	galaxy.addChild(galaxyCore)
	galaxy.setChildrenVisible(False)
	return (galaxy,galaxyCore)