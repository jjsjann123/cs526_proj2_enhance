from omega import *
from omegaToolkit import *
from fun import *
from xmlReader import *
from orbit import *
from multiples import *
from galaxy import *
from stars import *
from graph import *
from CoordinateCalculator import CoordinateCalculator

screenPosition = CoordinateCalculator()

newSystemInCave = None
allSystem = {}
globalOrbitScale = 5.0
globalRadiusScale = 0.5
globalRotationScale = 1.0
getSceneManager().displayWand(0, 1)
getSceneManager().setBackgroundColor(Color('black'))
sky = getStar()
skyScale = 6
sky.setScale(Vector3(1,1,1)*skyScale * globalOrbitScale)

mm = MenuManager.createAndInitialize()
appMenu = mm.createMenu("contolPanel")

appMenu.addButton("OrbitScale +", "changeOrbit(1.5)")
appMenu.addButton("OrbitScale -", "changeOrbit(1.0/1.5)")
appMenu.addButton("RadiusScale +", "changeRadius(1.5)")
appMenu.addButton("RadiusScale -", "changeRadius(1.0/1.5)")
appMenu.addButton("RotationSpeed +", "changeRotation(1.3)")
appMenu.addButton("RotationSpeed -", "changeRotation(1.0/1.3)")

appMenu.addButton("Show Galaxy", "switchSystemInCave(galaxy)")
appMenu.addButton("Reset View", "resetView()")

sub = appMenu.addSubMenu("Graph x_Axis")
button = sub.addButton("period", "planetGraph.switchXAxisByIndex(0)").getButton()
button.setRadio(True)
button = sub.addButton("semi-major axis", "planetGraph.switchXAxisByIndex(1)").getButton()
button.setRadio(True)
button = sub.addButton("eccentricity", "planetGraph.switchXAxisByIndex(2)").getButton()
button.setRadio(True)
button = sub.addButton("mass", "planetGraph.switchXAxisByIndex(3)").getButton()
button.setRadio(True)
button = sub.addButton("radius", "planetGraph.switchXAxisByIndex(4)").getButton()
button.setRadio(True)
button = sub.addButton("distance", "planetGraph.switchXAxisByIndex(5)").getButton()
button.setRadio(True)

sub = appMenu.addSubMenu("Graph y_Axis")
button = sub.addButton("period", "planetGraph.switchYAxisByIndex(0)").getButton()
button.setRadio(True)
button = sub.addButton("semi-major axis", "planetGraph.switchYAxisByIndex(1)").getButton()
button.setRadio(True)
button = sub.addButton("eccentricity", "planetGraph.switchYAxisByIndex(2)").getButton()
button.setRadio(True)
button = sub.addButton("mass", "planetGraph.switchYAxisByIndex(3)").getButton()
button.setRadio(True)
button = sub.addButton("radius", "planetGraph.switchYAxisByIndex(4)").getButton()
button.setRadio(True)
button = sub.addButton("distance", "planetGraph.switchYAxisByIndex(5)").getButton()
button.setRadio(True)

cam = getDefaultCamera()
cam.setControllerEnabled(False)
flagMoveBack = False
flagMoveForward = False
flagMoveUp = False
flagMoveDown = False
flagRotateUpDown = 0.0
flagRotateLeftRight = 0.0
speed = 5
omega = radians(30)
updateFuncList = []

flagShowSpot = False
spotLight = SphereShape.create(0.02, 4)
spotLight.setPosition(Vector3(0,0,0))
spotLight.setEffect("colored -e red")
cam.addChild(spotLight)
menuShow = False


def pickSystem(node):
	global containerToSystemMap
	global newSystemInCave
	print 'pick the system'
	pick = containerToSystemMap.get(node)
	if pick != None:
		print 'pick ', pick
		print 'node ', node
		switchSystemInCave(pick)
pickMultiples = pickSystem
btest = True
def ifHitAnything (node):
	global btest
	if (node == None):
		print "missed"
	else:
		print 'hit'
		if btest:
			node.setEffect("colored -e red")
		else:
			node.setEffect("colored -e blue")
		btest = not btest

def onUpdate(frame, t, dt):
	global cam
	global speed
	global omega
	global flagMoveBack
	global flagMoveForward
	global flagMoveUp
	global flagMoveDown
	global flagRotateUpDown
	global flagRotateLeftRight
	global updateFuncList
	
	#	Movement
	if(flagMoveForward):
		cam.translate(0, 0, -dt * speed, Space.Local )
	if(flagMoveBack):
		cam.translate(0, 0, dt * speed, Space.Local )
	if(flagMoveUp):
		cam.translate(0, dt * speed, 0, Space.Local )
	if(flagMoveDown):
		cam.translate(0, -dt * speed, 0, Space.Local )
	cam.pitch(flagRotateUpDown*omega*dt)
	cam.yaw(flagRotateLeftRight*omega*dt)
	
	dx = 0
	dy = 0
	graphSpeed = 0.1
	if(flagZoomInV):
		dy -= dt * graphSpeed
	if(flagZoomOutV):
		dy += dt * graphSpeed
	if(flagZoomInH):
		dx -= dt * graphSpeed
	if(flagZoomOutH):
		dx += dt * graphSpeed
	if(dx != 0 or dy != 0):
		planetGraph.increScale(dx, dy)
	
	planetGraph.pan(flagPanH*graphSpeed, flagPanV*graphSpeed)
	
	
	for func in updateFuncList:
		func(frame, t, dt)
		
	
	
def attachUpdateFunction(func):
	global updateFuncList
	updateFuncList.append(func)
	

def changeOrbit(ratio):
	global globalOrbitScale
	global sky
	global skyScale
	globalOrbitScale *= ratio
	setGlobalOrbitScale(globalOrbitScale)
	
def changeRadius(ratio):
	global globalRadiusScale
	globalRadiusScale *= ratio
	setGlobalRadiusScale(globalRadiusScale)

def changeRotation(ratio):
	global globalRotationScale
	globalRotationScale *= ratio
	
def resetView():
	cam = getDefaultCamera()
	cam.setPosition(Vector3( 10, 2, 10 ))
	cam.setPitchYawRoll(Vector3(0, radians(45), 0))
	cam.pitch(radians(-10))

def switchSystemInCave(newSystem):
	global systemInCave
	global galaxy
	global galaxyCore
	global planetGraph
	if isinstance(systemInCave, PlanetarySystem):
		allSystem[systemInCave.stellarName][1].setHighlight(False)
	if isinstance(newSystem, PlanetarySystem):
		allSystem[newSystem.stellarName][1].setHighlight(True)
	if newSystem == galaxy:
		systemInCave.setVisible(False)
		galaxy.setChildrenVisible(True)
		galaxy.setVisible(True)
		galaxyCore.getMaterial().setDepthTestEnabled(False)
		systemInCave = galaxy
		planetGraph.setHighlight(None)
	else:
		if galaxy.isVisible():
			galaxy.setVisible(False)
			galaxy.setChildrenVisible(False)
		if newSystem != None:
			if systemInCave != None and systemInCave != newSystem:
				systemInCave.setVisible(False)
			newSystem.setVisible(True)
			planetGraph.setHighlight(newSystem.stellarName)
		else:
			if systemInCave != None:
				systemInCave.setVisible(False)
			#planetGraph.setHighlight(None)
			
		systemInCave = newSystem
		if systemInCave != None:
			setGlobalOrbitScale(globalOrbitScale)
			setGlobalRadiusScale(globalRadiusScale)

def updateFunction(frame, t, dt):
	global systemInCave
	global newSystemInCave
	global galaxy
	global sky
	global globalRotationScale
	if newSystemInCave != None and newSystemInCave != systemInCave:
		print "switch it"
		switchSystemInCave(newSystemInCave)
		newSystemInCave = None
	if systemInCave != None and systemInCave != galaxy:
		systemInCave.running(dt*globalRotationScale)
	galaxy.yaw(dt*radians(5)*globalRotationScale)
	sky.yaw(dt*radians(5)*globalRotationScale)
	
def setGlobalOrbitScale(scale = 5.0):
	global globalOrbitScale
	globalOrbitScale = scale
	multiples.orbitScale.setFloat(scale)
	PlanetarySystem.orbitScale = scale
	sky.setScale(Vector3(1,1,1)*scale*skyScale)
	if systemInCave != None and systemInCave != galaxy:
		systemInCave.setOrbitScale()

def setGlobalRadiusScale(scale = 0.2):
	global globalRadiusScale
	globalRadiusScale = scale
	multiples.radiusScale.setFloat(scale)
	PlanetarySystem.radiusScale = scale
	if systemInCave != None and systemInCave != galaxy:
		systemInCave.setRadiusScale()

def setGlobalRotationScale(scale = 1.0):
	global globalRotationScale
	globalRotationScale = scale

def setRotationSpeedScale(scale):
	PlanetarySystem.speedScale = scale

def moveMultiple(x, y, z):
	print x, ' ', y, ' ', z
		
#
#	Here h and v should be in range(1,8)
#
def addMultipleToWall(multiple, h, v):
	global rootNode
	global column
	global row
	global cam
	if column < h or row < v:
		print "out of range"
		return None
	else:
		print "construct"
		multiple.multiple.setPosition(Vector3(-0.5, 0, 0.01) + multiple.multiple.getPosition())
		#if h >= 4:
		#	h+=3
		if h >= 2:
			h+=5
		v -= 1
		hLoc = h + 0.5
		degreeConvert = 36.0/360.0*2*pi #18 degrees per panel times 2 panels per viz = 36
		caveRadius = 3.25
		screenCenter = multiple.parentNode
		screenCenter.setPosition(Vector3(sin(hLoc*degreeConvert)*caveRadius, v * 0.29 + 0.41, cos(hLoc*degreeConvert)*caveRadius))
		screenCenter.yaw(hLoc*degreeConvert+radians(180))
		rootNode.addChild(screenCenter)
		return screenCenter

#
#	Read all files and initialize
#

cam = getDefaultCamera()
rootNode = SceneNode.create("systemOnWall")
cam.addChild(rootNode)
column = 6
row = 8
systemDir = "./stellar/"
multiples.initialize()
systemDic = readAllFilesInDir(systemDir)

multiples.radiusRatio.setFloat(4.0)
multiples.orbitRatio.setFloat(8.0)

# skybox = Skybox()
# skybox.loadCubeMap('./model/skybox/', 'png')
# getSceneManager().setSkyBox(skybox)
cam.setPosition(Vector3( 10, 2, 10 ))
cam.yaw(radians(45))
cam.pitch(radians(-10))


##########################################
#
#  Graph Part
#
##########################################
ui = UiModule.createAndInitialize()
wf = ui.getWidgetFactory()
uiroot = ui.getUi()
hitPlanet = None
lastHitPlanet = None

x = 1366*12
y = 0
width = 1366*4
height = 768*4
iconX = 100
iconY = 100

planetGraph = buildGraph(systemDic, ui, x, y, width, height, iconX, iconY)

c = planetGraph.container
img = c.getChildByIndex(0)

list = planetGraph.planetList

indicator = Image.create(uiroot)
indicator.setData(loadImage('./dot.png'))
indicator.setSize(Vector2(50,50))
indicator.setVisible(False)
flagZoomInV = False
flagZoomOutV = False
flagZoomInH = False
flagZoomOutH = False
flagPanH = 0
flagPanV = 0

# for h in range(1,9):
	# for v in range(1,9):
		# outlineBox = SphereShape.create(0.125, 4)
		# addMultipleToWall( outlineBox, h, v)
def loadAllSystem():
	h = 1;
	v = 0;
	global galaxy
	global galaxyCore
	global containerToSystemMap
	global targetList
	(galaxy,galaxyCore) = buildGalaxy(systemDic)
	for systemName in systemDic:
		stellar = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
		stellarMultiple = multiples(systemDic[systemName])
		v+=1;
		if v > row:
			v = 1
			h+=1
		addMultipleToWall(stellarMultiple, h, v)
		stellar.drawSystem(False)
		allSystem.update( {systemName: [stellar, stellarMultiple]} )
		stellarMultiple.multiple.setSelectable(True)
		targetList.append(stellarMultiple.multiple)
		containerToSystemMap.update( {stellarMultiple.multiple: stellar} )
		if v == row and h == column:
			break;
def onEvent():
	global cam
	global flagMoveBack
	global flagMoveForward
	global flagMoveUp
	global flagMoveDown
	global flagRotateUpDown
	global flagRotateLeftRight
	global spotLight
	global pickMultiples
	global targetList
	global appMenu
	global menuShow
	global containerToSystemMap
	global newSystemInCave
	
	global screenPosition
	global indicator
	global planetGraph
	global hitPlanet
	global lastHitPlanet
	global flagZoomInV
	global flagZoomOutV
	global flagZoomInH
	global flagZoomOutH
	global flagPanH
	global flagPanV
	global allSystem
	
	e = getEvent()
	type = e.getServiceType()
	if(type == ServiceType.Pointer or type == ServiceType.Wand or type == ServiceType.Keyboard):
		# Button mappings are different when using wand or mouse
		

		if(type == ServiceType.Keyboard):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button1
			lowHigh = 0
			leftRight = 0
			forward = ord('w')
			down = ord('s')
			low = ord('i')
			high = ord('k')
			turnleft = ord('j')
			turnright = ord('l')
			climb = ord('a')
			descend = ord('d')
			flagH = False
			flagV = False
			if(e.isKeyDown( low)):
				lowHigh = 0.5
				flagV = True
			if(e.isKeyDown( high )):
				lowHigh = -0.5
				flagV = True
			if(e.isKeyDown( turnleft)):
				leftRight = 0.5
				flagH = True
			if(e.isKeyDown( turnright )):
				leftRight = -0.5				
				flagH = True
			if(e.isKeyDown( forward)):
				flagMoveForward = True
			if(e.isKeyDown( down )):
				flagMoveBack = True
			if(e.isKeyDown( climb)):
				flagMoveUp = True
			if(e.isKeyDown( descend )):
				flagMoveDown = True
			if(e.isKeyUp( forward)):
				flagMoveForward = False
			if(e.isKeyUp( down )):
				flagMoveBack = False
			if(e.isKeyUp( climb)):
				flagMoveUp = False
			if(e.isKeyUp( descend )):
				flagMoveDown = False
			flagRotateLeftRight = leftRight
			flagRotateUpDown = lowHigh

		if(type == ServiceType.Wand):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button3
			forward = EventFlags.ButtonUp
			down = EventFlags.ButtonDown
			climb = EventFlags.ButtonLeft
			descend = EventFlags.ButtonRight
			pick = EventFlags.Button5
			move = EventFlags.Button7
			lowHigh = e.getAxis(1)
			leftRight = -e.getAxis(0)
			
			pos = e.getPosition()
			orient = e.getOrientation()
			refVec = Vector3(0.0, 0.0, -1.0)
			v = orient * refVec
			screenPosition.set_position(pos[0], pos[1], pos[2])
			screenPosition.set_orientation(v.x, v.y, v.z)
			screenPosition.calculate()
			screenX = screenPosition.get_x()
			screenY = screenPosition.get_y()
			pixelX = int(screenX * 24588)
			pixelY = int(screenY *  3072)
			indicator.setCenter(Vector2(pixelX, pixelY))
			pos2d = Vector2(pixelX, pixelY)
			if (planetGraph.container.hitTest(pos2d)):
				
				if not indicator.isVisible():
					indicator.setVisible(True)
					flagMoveBack = False
					flagMoveForward = False
					flagMoveUp = False
					flagMoveDown = False
					flagRotateUpDown = 0.0
					flagRotateLeftRight = 0.0
				indicator.setCenter(pos2d)
				offset = planetGraph.container.getPosition() + planetGraph.graphContainer.getPosition()
				#if hitPlanet == None:
				#	oldLength = 100
				#else:
				#	oldLength = (pos2d - hitPlanet.img.getPosition()).magnitude
				
				if hitPlanet == None:
					oldLength = 10000
				else:
					oldLength = (pos2d - hitPlanet.img.getCenter() - offset).magnitude()
				hit = False
				for planet in planetGraph.planetList:
					planetInstance = planetGraph.planetList[planet]
					if (planetInstance.img.hitTest(pos2d) ):
						hit = True
						newLength = (pos2d - planetInstance.img.getCenter() - offset).magnitude()
						if newLength < oldLength:
							if hitPlanet != None:
								hitPlanet.setActivate(False)
							planetInstance.setActivate(True)
							hitPlanet = planetInstance
							oldLength = newLength
				
				if hit == False and hitPlanet != None:
					hitPlanet.setActivate(False)
					hitPlanet = None
				
				if(hit and e.isButtonDown(pick)):
					print "hit planet: " , hitPlanet.data['name'], " in stellar: ", hitPlanet.data['stellarName']
					newSystemInCave = allSystem[hitPlanet.data['stellarName']][0]

				if(e.isButtonDown( forward)):
					flagZoomInV = True
				if(e.isButtonDown( down )):
					flagZoomOutV = True
				if(e.isButtonDown( climb)):
					flagZoomInH = True
				if(e.isButtonDown( descend )):
					flagZoomOutH = True
				if(e.isButtonUp( forward)):
					flagZoomInV = False
				if(e.isButtonUp( down )):
					flagZoomOutV = False
				if(e.isButtonUp( climb)):
					flagZoomInH = False
				if(e.isButtonUp( descend )):
					flagZoomOutH = False
				flagPanH = e.getAxis(0)
				flagPanV = e.getAxis(1)
				
				e.setProcessed()
			else:
				indicator.setVisible(False)
				flagZoomInV = False
				flagZoomOutV = False
				flagZoomInH = False
				flagZoomOutH = False
				flagPanH = 0
				flagPanV = 0			
		
		if(type == ServiceType.Wand and not e.isProcessed() ):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button3
			forward = EventFlags.ButtonUp
			down = EventFlags.ButtonDown
			climb = EventFlags.ButtonLeft
			descend = EventFlags.ButtonRight
			pick = EventFlags.Button5
			move = EventFlags.Button7
			lowHigh = e.getAxis(1)
			leftRight = -e.getAxis(0)
			
			if(e.isButtonDown(confirmButton) and not menuShow):
				appMenu.getContainer().setPosition(e.getPosition())
				appMenu.show()
				appMenu.placeOnWand(e)
				menuShow = True
			if(e.isButtonDown(quitButton) and menuShow):
				appMenu.hide()
				menuShow = False
			e.setProcessed()

			if(e.isButtonDown( forward)):
				flagMoveForward = True
			if(e.isButtonDown( down )):
				flagMoveBack = True
			if(e.isButtonDown( climb)):
				flagMoveUp = True
			if(e.isButtonDown( descend )):
				flagMoveDown = True
			if(e.isButtonUp( forward)):
				flagMoveForward = False
			if(e.isButtonUp( down )):
				flagMoveBack = False
			if(e.isButtonUp( climb)):
				flagMoveUp = False
			if(e.isButtonUp( descend )):
				flagMoveDown = False
			flagRotateLeftRight = leftRight
			flagRotateUpDown = lowHigh

			if flagShowSpot:
				pos = e.getPosition()
				orient = e.getOrientation()
				wandPos = Point3(pos[0], pos[1], pos[2])
				Ray = orient * Ray3(wandPos, Vector3( 0., 0., -1.))
				wall = Sphere(Point3(0., 0., 0.), 3.45)
				res = Ray.intersect(wall)
			# r = getRayFromEvent(e)
			# if (r[0]): 
				# ray = Ray3(Point3(r[1][0], r[1][1], r[1][2]), Vector3(r[2][0], r[2][1], r[2][2]))
				# pos = cam.getPosition()
				# wall = Sphere(Point3(pos[0], pos[1], pos[2]), 3.45)
				# res = ray.intersect(wall)
				if res != None:
					hitSpot = res.p
					spotLight.setPosition(Vector3(hitSpot[0], hitSpot[1], hitSpot[2]))
				# if(e.isButtonDown(pick) and pickMultiples != None):
					# camPos = cam.getPosition()
					# pos = e.getPosition()
					# wandPos = Point3(pos[0], pos[1], pos[2]) + Point3(camPos[0], camPos[1], camPos[2])
					# orient = e.getOrientation()
					# ray = cam.getOrientation() * orient * Ray3(Point3(wandPos[0], wandPos[1], wandPos[2]), Vector3( 0., 0., -1.))
					# querySceneRay(ray.p, ray.v, pickMultiples)
						
			if(e.isButtonDown(pick) and targetList != [] and pickMultiples != None):
				r = getRayFromEvent(e)
				print "start finding"
				for item in targetList:
					hitData = hitNode(item, r[1], r[2])
					if(hitData[0]):
						newSystemInCave = containerToSystemMap.get(item)
						#switchSystemInCave(containerToSystemMap.get(item))
						#break

		if(type == ServiceType.Pointer and not e.isProcessed() ):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button1
			#newSystemInCave = containerToSystemMap.get(targetList[2])
			if(e.isButtonDown(confirmButton)):
				appMenu.getContainer().setPosition(e.getPosition())
				appMenu.show()
				appMenu.placeOnWand(e)
			if(e.isButtonDown(quitButton)):
				appMenu.hide()
			e.setProcessed()
			if flagShowSpot:
				pos = e.getPosition()
				orient = e.getOrientation()
				#Ray = orient * Ray3(Point3(pos[0], pos[1], pos[2]), Vector3( 0., 0., -1.))
				Ray = Ray3(Point3(pos[0], pos[1], pos[2]), Vector3( 0., 0., -1.))
				wall = Sphere(Point3(0., 0., 0.), 3.45)
				res = Ray.intersect(wall)
				# r = getRayFromEvent(e)
				# if (r[0]): 
					# ray = Ray3(Point3(r[1][0], r[1][1], r[1][2]), Vector3(r[2][0], r[2][1], r[2][2]))
					# pos = cam.getPosition()
					# wall = Sphere(Point3(pos[0], pos[1], pos[2]), 3.45)
					# res = ray.intersect(wall)
				if res != None:
					hitSpot = res.p
					print "moving sphere"
					spotLight.setPosition(Vector3(hitSpot[0], hitSpot[1], hitSpot[2]))
			# camPos = cam.getPosition()
			# pos = e.getPosition()
			# wandPos = Point3(pos[0], pos[1], pos[2]) + Point3(camPos[0], camPos[1], camPos[2])
			# orient = e.getOrientation()
			# print cam.getOrientation()
			# print orient
			# print wandPos
			# ray = cam.getOrientation() * orient * Ray3(Point3(wandPos[0], wandPos[1], wandPos[2]), Vector3( 0., 0., -1.))
			# print ray
			# if pickMultiples != None:
				# querySceneRay(ray.p, ray.v, pickMultiples)
	
setEventFunction(onEvent)
setUpdateFunction(onUpdate)

loadAllSystem()
switchSystemInCave(allSystem['Sun'][0])
attachUpdateFunction(updateFunction)
sky.getMaterial().setDepthTestEnabled(False)
#(galaxy, galaxyCore) = buildGalaxy(systemDic)
#systemName = "Kepler-33"
#stellar = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
#stellarMultiple = multiples(systemDic[systemName])
#stellarMultiple.parentNode.setPosition(Vector3( -2, 2, -4))
#stellar.drawSystem(False)
#systemName = "Sun"
#stellar2 = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
#stellarMultiple2 = multiples(systemDic[systemName])
#stellarMultiple2.parentNode.setPosition(Vector3( 0.5, 2, -4))
#stellar2.drawSystem(False)
#switchSystemInCave(stellar2)
