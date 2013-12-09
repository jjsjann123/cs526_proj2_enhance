from omega import *
from cyclops import *
from math import *
from euclid import *
from fun import *

class multiples(object):
	
	global stellarColorMap
	
	orbitScale = Uniform.create('orbitScale', UniformType.Float, 1)
	radiusScale = Uniform.create('radiusScale', UniformType.Float, 1)
	orbitRatio = Uniform.create('orbit_ratio', UniformType.Float, 1)
	radiusRatio = Uniform.create('radius_ratio', UniformType.Float, 1)
	#glowPower = Uniform.create('unif_Glow', UniformType.Float, 1)
	#starColor = Uniform.create('star_color', UniformType.Color, 1)
	cutOffX = Uniform.create('cutoff_x', UniformType.Float, 1)
	cutOffY = Uniform.create('cutoff_y', UniformType.Float, 1)
	
	offPanelSize = Uniform.create('off_size', UniformType.Float, 1)

	multipleScale = 0.05
	height = 5.0
	width = 40.0
	offsize = 0.2
	orbitRatioFloat = 10.0
	radiusRatioFloat = 4.0
	
	ratioRadius = 20.0
	fontSize = 0.7
	
	@staticmethod
	def getData(str, type, default):
		if str == None:
			return default
		else:
			return type(str)

	@classmethod
	def initialize(cls):
		multipleScale = cls.multipleScale
		width = cls.width * multipleScale
		height = cls.height * multipleScale
		
		cls.orbitScale.setFloat(1.0)
		cls.orbitRatio.setFloat(cls.orbitRatioFloat)
		cls.radiusRatio.setFloat(cls.radiusRatioFloat)
		cls.radiusScale.setFloat(1.0)
		#cls.glowPower.setFloat(20)
		#cls.starColor.setColor(Color(1, 0, 0, 1))
		cls.cutOffX.setFloat(width - cls.offsize*multipleScale)
		cls.cutOffY.setFloat(height - cls.offsize*multipleScale)
		cls.offPanelSize.setFloat(cls.offsize * cls.multipleScale)
		geom = ModelGeometry.create('stellar')
		v1 = geom.addVertex(Vector3(0, height/2, -0.01))
		geom.addColor(Color(0,1,0,0))
		v2 = geom.addVertex(Vector3(0, -height/2, -0.01))
		geom.addColor(Color(0,0,0,0))
		v3 = geom.addVertex(Vector3(width, height/2, -0.01))
		geom.addColor(Color(1,1,0,0))
		v4 = geom.addVertex(Vector3(width, -height/2, -0.01))
		geom.addColor(Color(1,0,0,0))
		geom.addPrimitive(PrimitiveType.TriangleStrip, 0, 4)
		getSceneManager().addModel(geom)

		shaderPath = "./shaders/"
		multipleDraw = ProgramAsset()
		multipleDraw.name = "background"
		multipleDraw.vertexShaderName = shaderPath + "background.vert"
		multipleDraw.fragmentShaderName = shaderPath + "background.frag"
		getSceneManager().addProgram(multipleDraw)

		starDraw = ProgramAsset()
		starDraw.name = "planet"
		starDraw.vertexShaderName = shaderPath + "planet.vert"
		starDraw.fragmentShaderName = shaderPath + "planet.frag"
		starDraw.geometryOutVertices = 4
		starDraw.geometryShaderName = shaderPath + "/planet.geom"
		starDraw.geometryInput = PrimitiveType.Points
		starDraw.geometryOutput = PrimitiveType.TriangleStrip
		getSceneManager().addProgram(starDraw)

	def setHighlight(self, bool):
		if bool:
			self.highlight.setInt(2)
		else:
			self.highlight.setInt(0)
		
	def __init__(self, system):
		multiple = StaticObject.create('stellar')
		multiple.setEffect("background -t")
		self.multiple = multiple
		self.multiple.setSelectable(True)
		self.starRadius = system['star'][0]['radius']
		#	This is supposed to be set to the parentNode for it to attach to.
		self.parentNode = SceneNode.create('stellar_'+system['stellar']['name'])
		self.parentNode.addChild(multiple)
		multiple.getMaterial().addUniform('unif_Glow', UniformType.Float).setFloat(1/self.starRadius*self.ratioRadius)

		stellar = system['stellar']
		distance = self.getData(stellar['distance'], float, 100.0)
		name = self.getData(stellar['name'], str, 'anonym')
		spectraltype = self.getData(system['star'][0]['spectraltype'], str, 'G')
		(min, max) = habitRange[spectraltype]
		material = multiple.getMaterial()
		self.highlight = Uniform.create('highlight', UniformType.Int, 1)
		self.highlight.setInt(0)
		material.addUniform('star_color', UniformType.Color).setColor(stellarColorMap[spectraltype])
		material.attachUniform(self.orbitScale)
		material.attachUniform(self.cutOffX)
		material.attachUniform(self.orbitRatio)
		material.attachUniform(self.highlight)
		material.addUniform('hab_min', UniformType.Float).setFloat(min*self.multipleScale)
		material.addUniform('hab_max', UniformType.Float).setFloat(max*self.multipleScale)
		
		
		multipleScale = self.multipleScale
		width = self.width * multipleScale
		height = self.height * multipleScale
		#info = 'Stellar System: ' + name + ' Distance: ' + str(round(distance,1))
		info = name + ' distance from earth ' + str(round(distance,1))
		t = Text3D.create( 'fonts/arial.ttf', self.fontSize * self.multipleScale, info )
		t.setFixedSize(False)
		t.setFontResolution(120)
		t.setPosition(Vector3(-0.5, height/2, 0))
		t.setPosition(Vector3(-0.5, height/2, 0))
		self.parentNode.addChild(t)
		planets = system['planets']
		numOfPlanets = len(planets)
		geom = ModelGeometry.create(name)
		index = 0
		for planet in planets:
			geom.addVertex(Vector3(self.multipleScale * self.getData(planet['semimajoraxis'], float, 1), 0, 0.01))
			geom.addColor(Color(discoveryMethod[planet['discoverymethod']], numOfPlanets, index, self.multipleScale * self.getData(planet['radius'], float, 0.1)))
			# pName = planet['name']
			# print pName
			index += 1
			# if name in textureMap:
				# obj.setEffect("textured -d ./model/" + name + ".jpg")
			# else:
				# obj.setEffect("textured -d " + randomTextureMap[hash_string(name,len(randomTextureMap))] )
			# multiple.getMaterial().setDiffuseTexture(
		geom.addVertex(Vector3(width, 0., 0.01))
		geom.addColor(Color(10.0, 0.0, 0.0, 0.0))
		geom.addPrimitive(PrimitiveType.Points, 0, numOfPlanets+1)
		getSceneManager().addModel(geom)
		planetSystem = StaticObject.create(name)
		planetSystem.setEffect("planet -t")
		material = planetSystem.getMaterial()
		material.attachUniform(self.orbitScale)
		material.attachUniform(self.radiusScale)
		material.attachUniform(self.cutOffX)
		material.attachUniform(self.cutOffY)
		material.attachUniform(self.offPanelSize)
		material.attachUniform(self.orbitRatio)
		material.attachUniform(self.radiusRatio)
		multiple.addChild(planetSystem)