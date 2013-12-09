from omega import *
from cyclops import *
from math import *
from euclid import *


class PlanetarySystem(object):
	attributeList = []
	viewNode = None
	panelNode = None
	
	fineLevel = 8	#	fine level stays between 0 to 10
	
	orbitScale = 1.0
	radiusScale = 1.0
	speedScale = 5.0
	
	orbitParameter = { 'name' : 'planetName', 'star' : 'hostName', 'orbit': 'semi-MajorAxis[AU]', 'size': 'pl_rade', 'year': 'orbitPeriod[years]', 'day': 'rotationPeriod[days]', 'obliquity': 'rotationTilt[deg]', 'inclination': 'inclination[deg]', 'eccentricity': 'eccentricity' }
	index = {}

	def __init__(self):
		self.starList = []
		self.planetList = []
		self.totalDiameter = 0
		self.sphereScaleNode = SceneNode.create(str(id(self)))
		
		#	planetObjList stores the current angle, location and other information of each planet:
		#		name: obj, theta, 
		self.planetObjList = {}
		#self.orbitScaleNode = SceneNode.create(id(self))
	@classmethod
	def initialize(cls, str):
		cls.attributeList = str.split(',')
		for key in cls.orbitParameter:
			cls.index.update ( { key: cls.attributeList.index(cls.orbitParameter[key]) } )
		cls.panelNode = SceneNode.create('panelView')
		cls.viewNode = SceneNode.create('mainView')
	@staticmethod
	def getElipsePosition(theta, majorAxis, eccentricity, inclination, periastron = 0.0, ascendingNode = 0.0):
		radius = majorAxis * (1 - eccentricity*eccentricity) / (1- eccentricity*cos(radians(theta)))
		x = cos(radians(theta-periastron)) * cos(radians(inclination)) * radius
		y = sin(radians(theta-periastron)) * radius
		z = cos(radians(theta-periastron)) * sin(radians(inclination)) * radius
		r = sqrt( x**2 + y**2 )
		thetaPrime = radians(theta-periastron) + radians(ascendingNode)
		x = r * cos(thetaPrime)
		y = r * sin(thetaPrime)
		return Vector3(x, z, y)
	def setPlanetPosition(self, theta, name):
		target = self.planetObjList[name]
		if theta > 360.0:
			theta -= 360.0
		target[0] = theta
		target[1].setPosition( self.getElipsePosition( theta, target[4], target[6], target[5] ) )
		
	def planetRotate(self, delta, name):
		target = self.planetObjList[name]
		target[0] += delta
		if target[0] > 360.0:
			target[0] -= 360.0
		target[1].setPosition( self.getElipsePosition( target[0], target[4], target[6], target[5] ) )

	def add(self, attrStr):
		attribute = attrStr.split(',')
		if (attribute[0] != attribute[1]):
			self.planetList.append(attribute)
		else:
			self.starList.append(attribute)
	def drawSystem(self):
		self.orbitLine = LineSet.create()
		self.orbitLine.setEffect('colored -e green')
		#self.testLine = LineSet.create()
		#self.testLine.setEffect('colored -e green')
		for star in self.starList:
			self.drawStar( star )
		for planet in self.planetList:
			self.drawPlanet( planet )
	def drawPlanet(self, planet):
		# Draw orbit
		# Segments # is defined by fineLevel
		#		1 - 36 up to 10 - 360
		index = self.index
		majorAxis = float(planet[index['orbit']]) * self.orbitScale
		inclination = float(planet[index['inclination']])
		eccentricity = float(planet[index['eccentricity']])
		if self.fineLevel > 0:
			interval = 10.0 / self.fineLevel
			theta = 0.0
			#radius = float(planet[self.index['orbit']]) * self.orbitScale
			#eccentricity = 0.70
			while theta <= 360:
				line = self.orbitLine.addLine()
				line.setStart (self.getElipsePosition(theta, majorAxis, eccentricity, inclination) )
				theta += interval
				line.setEnd (self.getElipsePosition(theta, majorAxis, eccentricity, inclination) )
				# radius = majorAxis
				# tx = cos(radians(theta)) * radius
				# ty = sin(radians(theta)) * radius
				# theta += interval
				# tnx = cos(radians(theta)) * radius
				# tny = sin(radians(theta)) * radius
				# line = self.orbitLine.addLine()
				# line.setStart (Vector3(tx, 0, ty))
				# line.setEnd(Vector3(tnx, 0, tny))
		
		#	Draw planets
		name = planet[index['name']]
		phase = 0
		size = float(planet[index['size']]) * self.radiusScale
		#obj = SphereShape.create(size, 4)
		obj = BoxShape.create(size, size, size)
		year = float(planet[index['year']])
		day = float(planet[index['day']])
		tilt = float(planet[index['obliquity']])
		self.planetObjList.update({ name: [phase, obj, year, day, majorAxis, inclination, eccentricity]})
		self.setPlanetPosition( 0, name)
	
	def drawStar(self, star):
		print "Star"
		
def readPlanetarySystemFile(filename, dir = None):
	if ( dir != None ):
		filename = dir + filename
	f = open(filename)
	file = [line.rstrip('\n') for line in f]
	ret = {}
	for line in file:
		ret.update( { line: PlanetarySystem() } )
	return ret

def readPlanetsFile(planetarySystemList, filename, dir = None):
	if ( dir != None ):
		filename = dir + filename
	f = open(filename)
	file = [line.rstrip('\n') for line in f]
	firstLine = True
	for line in file:
		if firstLine == True:
			firstLine = False
			PlanetarySystem.initialize(line)
		elif line[0] != '#':
			attribute = line.partition(',')
			planetarySystemList[attribute[0]].add(line)
			
def drawPlanetarySystems(planetarySystemList):
	for pSys in planetarySystemList:
		planetarySystemList[pSys].drawSystem()