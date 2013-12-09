from omega import *
from cyclops import *
from math import *
from euclid import *
from fun import *
import os

scene = getSceneManager()
textureSphere = ModelInfo()
textureSphere.name = "textureSphere"
textureSphere.path = "./model/sphere.obj"
scene.loadModel(textureSphere)

light = []
light.append(Light.create())
light[0].setLightType(LightType.Point)
light[0].setColor(Color(0.0, 0.0, 0.0, 0.0))
light[0].setPosition(Vector3(0.0, 0.0, 0.0))
light[0].setEnabled(True)

shaderPath = "./shaders/"
habitZoneDraw = ProgramAsset()
habitZoneDraw.name = "habit"
habitZoneDraw.vertexShaderName = shaderPath + "habit.vert"
habitZoneDraw.fragmentShaderName = shaderPath + "habit.frag"
getSceneManager().addProgram(habitZoneDraw)


class PlanetarySystem(object):
	global light
	global textureMap
	global starTextureMap
	global starTextureDir
	global habitRange
	global radiusOfEarth
	global fontSize
	fineLevel = 10	#	fine level stays between 0 to 10
	orbitScale = 1.0
	radiusScale = 1.0
	speedScale = 1.0
	ratio = 10.0
	lineThickness = 0.01
	
	
	
	def __init__(self, star, planets, name):
		self.starList = star
		self.planetList = planets
		self.stellarName = name
		self.sphereScaleNode = SceneNode.create(name)
		self.starNode = SceneNode.create(name+'_star')
		self.allText = []
		print "draw", " ", name
		self.orbitLineList = []
		self.orbitLine = LineSet.create()
		self.orbitLine.setEffect('colored -e #FFFF66')
		#	planetObjList stores the current angle, location and other information of each planet:
		#		name: obj, theta, 
		self.planetObjList = {}
		#self.orbitScaleNode = SceneNode.create(id(self))
	def setVisible(self, visFlag= False):
		self.sphereScaleNode.setChildrenVisible(visFlag)
		self.starNode.setChildrenVisible(visFlag)
		self.orbitLine.setVisible(visFlag)
		if visFlag == True:
			light[0].setColor(Color(1.0, 1.0, 1.0, 1.0))
			for text in self.allText:
				text.setFacingCamera(getDefaultCamera())
		else:
			light[0].setColor(Color(0.0, 0.0, 0.0, 0.0))
	def setRadiusScale(self):
		list = self.planetObjList
		for planet in list:
			list[planet][1].setScale(Vector3(1,1,1)*self.radiusScale/self.orbitScale*list[planet][9])
	def setOrbitScale(self):
		self.orbitLine.setScale(Vector3(1,1,1)*self.orbitScale)
		self.sphereScaleNode.setScale(Vector3(1,1,1)*self.orbitScale)
		self.setRadiusScale()
		for seg in self.orbitLineList:
			seg.setThickness( self.lineThickness / self.orbitScale )
	@staticmethod
	def getData(str, type, default):
		if str == None:
			return default
		else:
			return type(str)
	@staticmethod
	def getElipsePosition(theta, majorAxis, eccentricity, inclination, periastron = 0.0, ascendingNode = 0.0):
		radius = majorAxis * (1 - eccentricity*eccentricity) / (1- eccentricity*cos(radians(theta)))
		x = cos(radians(theta-periastron)) * cos(radians(inclination)) * radius
		y = sin(radians(theta-periastron)) * radius
		z = cos(radians(theta-periastron)) * sin(radians(inclination)) * radius
		#x = x * cos(ascendingNode) - y * sin(ascendingNode)
		#y = x * sin(ascendingNode) + y * cos(ascendingNode)
		return Vector3(x, z, y).rotate_around(Vector3(0,1,0), radians(ascendingNode))
	def setPlanetPosition(self, theta, name):
		target = self.planetObjList[name]
		if theta > 360.0:
			theta -= 360.0
		target[0] = theta
		target[1].setPosition( self.getElipsePosition( theta, target[4], target[6], target[5], target[7], target[8] ) )
	def running(self, dt):
		planetList = self.planetObjList
		self.starNode.yaw(dt)
		for name in planetList:
			self.planetRotate(1000 * dt * self.speedScale /planetList[name][2], name)
			planetList[name][1].yaw(radians(1000 * dt * self.speedScale /planetList[name][3]))
	def planetRotate(self, delta, name):
		target = self.planetObjList[name]
		target[0] += delta
		if target[0] > 360.0:
			target[0] -= 360.0
		target[1].setPosition( self.getElipsePosition( target[0], target[4], target[6], target[5], target[7], target[8]  ) )
	def drawSystem(self, visFlag = False):
		#self.testLine = LineSet.create()
		#self.testLine.setEffect('colored -e green')
		for star in self.starList:
			self.drawStar( star )
		for planet in self.planetList:
			self.drawPlanet( planet )
		self.setVisible(visFlag)
	def drawPlanet(self, planet):
		# Draw orbit
		# Segments # is defined by fineLevel
		#		1 - 36 up to 10 - 360
		majorAxis = self.getData( planet['semimajoraxis'], float, 1.0)
		inclination = self.getData( planet['inclination'], float, 0.0 )
		eccentricity = self.getData( planet['eccentricity'], float, 0.0 )
		periastron = self.getData( planet['periastron'], float, 0.0 )
		ascendingnode = self.getData( planet['ascendingnode'], float, 0.0 )
		radius = self.getData( planet['radius'], float, 0.0 )
		year = self.getData(planet['period'], float, 365.0)
		day = self.getData(planet['day'], float, 1.0)
		tilt = self.getData(planet['axistilt'], float, 0.0)
		#
		#	Draw orbits.
		#
		if self.fineLevel > 0:
			interval = 10.0 / self.fineLevel
			theta = 0.0
			while theta <= 360:
				line = self.orbitLine.addLine()
				line.setStart (self.getElipsePosition(theta, majorAxis, eccentricity, inclination, periastron, ascendingnode) )
				theta += interval
				line.setEnd (self.getElipsePosition(theta, majorAxis, eccentricity, inclination, periastron, ascendingnode) )
				self.orbitLineList.append(line)
				line.setThickness( self.lineThickness / self.orbitScale )
		#
		#	Draw planets
		#
		name = planet['name']
		phase = 0
		#obj = SphereShape.create(radius, 4)
		#obj = BoxShape.create(radius, radius, radius)
		obj = StaticObject.create("textureSphere")
		if name in textureMap:
			obj.setEffect("textured -d ./model/" + name.lower() + ".jpg")
		else:
			obj.setEffect("textured -d " + randomTextureMap[hash_string(name,len(randomTextureMap))] )
		#obj.setScale(radius, radius, radius)
		#obj.pitch(radians(tilt))
		
		t = Text3D.create( 'fonts/arial.ttf', fontSize, name )
		t.setPosition(Vector3(0 , 1.5, 0))
		t.setFixedSize(True)
		t.setFontResolution(80)
		#t.setFacingCamera(getDefaultCamera())
		self.allText.append(t)

		axis = LineSet.create()
		axis.setEffect("colored -e white")
		line = axis.addLine()
		line.setStart( Vector3( 0., -1.5, 0.))
		line.setEnd( Vector3( 0., 1.5, 0.))
		line.setThickness(self.lineThickness)
		
		targetRoot = SceneNode.create(name)
		targetRoot.addChild(t)
		targetRoot.addChild(obj)
		targetRoot.setScale(Vector3(radius, radius, radius))
		targetRoot.pitch(radians(tilt))
		targetRoot.addChild(axis)
		
		#self.sphereScaleNode.addChild(obj)
		#self.planetObjList.update({ name: [phase, obj, year, day, majorAxis, inclination, eccentricity, periastron, ascendingnode, radius]})
		self.sphereScaleNode.addChild(targetRoot)
		self.planetObjList.update({ name: [phase, targetRoot, year, day, majorAxis, inclination, eccentricity, periastron, ascendingnode, radius, line, axis]})
		self.setPlanetPosition( 0, name)
	def drawStar(self, star):
		height = 1
		obj = StaticObject.create("textureSphere")
		radius = star['radius']
		obj.setScale(Vector3(radius, radius, radius) * 0.3)
		obj.setPosition(Vector3(0, height, 0))
		obj.setEffect("textured -v emissive -d " + starTextureDir + starTextureMap[star['spectraltype']])
		self.starNode.addChild(obj)
		
		t = Text3D.create( 'fonts/arial.ttf', fontSize*2, star['name'] )
		t.setPosition(Vector3(0 , height - radius * 0.3 - 0.1 , 0))
		t.setFixedSize(True)
		t.setFontResolution(80)
		#t.setFacingCamera(getDefaultCamera())
		self.starNode.addChild(t)
		self.allText.append(t)

		axis = LineSet.create()
		axis.setEffect("colored -e white")
		line = axis.addLine()
		line.setStart( Vector3( 0., height, 0.))
		line.setEnd( Vector3( 0., 0, 0.))
		line.setThickness(self.lineThickness)
		self.starNode.addChild(axis)
		
		(min, max) = habitRange[star['spectraltype']]
		habitZone = PlaneShape.create( max*2, max*2 )
		habitZone.pitch(radians(270))
		self.sphereScaleNode.addChild(habitZone)
		habitZone.setEffect("habit -d #66CCFF -t")
		habitZone.getMaterial().addUniform('ratio', UniformType.Float).setFloat(min/max)
		habitZone = PlaneShape.create( max*2, max*2 )
		habitZone.pitch(radians(90))
		self.sphereScaleNode.addChild(habitZone)
		habitZone.setEffect("habit -d #66CCFF -t")
		habitZone.getMaterial().addUniform('ratio', UniformType.Float).setFloat(min/max)