from omega import *
from cyclops import *
from omegaToolkit import *
from math import *
from euclid import *
from fun import *


appMenu.addButton("OrbitScale +", "changeOrbit(1.5)")
appMenu.addButton("OrbitScale -", "changeOrbit(1.0/1.5)")
appMenu.addButton("RadiusScale +", "changeRadius(1.5)")
appMenu.addButton("RadiusScale -", "changeRadius(1.0/1.5)")

appMenu.addButton("Show Galaxy", "switchSystemInCave(galaxy)")
appMenu.addButton("Reset View", "resetView()")

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
			leftRight = e.getAxis(0)
			
			if(e.isButtonDown(confirmButton)):
				appMenu.getContainer().setPosition(e.getPosition())
				appMenu.show()
				appMenu.placeOnWand(e)
			if(e.isButtonDown(quitButton)):
				appMenu.hide()
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
						pickMultiples(item)
						break
						
						

		if(type == ServiceType.Pointer):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button1
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
	for func in updateFuncList:
		func(frame, t, dt)
	
def attachUpdateFunction(func):
	global updateFuncList
	updateFuncList.append(func)
	
setEventFunction(onEvent)
setUpdateFunction(onUpdate)


# pickMultiples = ifHitAnything

# sphere2 = SphereShape.create(1, 4)
# sphere2.setPosition(Vector3(0, 3, -10))
# sphere2.setSelectable(True)
# cam.addChild(sphere2)
# sphere3 = SphereShape.create(1, 4)
# sphere3.setPosition(Vector3(3, 3, -10))

# geom = ModelGeometry.create('stellar')
# width = 2;
# height = 0.25;
# v1 = geom.addVertex(Vector3(0, height/2, -0.01))
# geom.addColor(Color(0,1,0,0))
# v2 = geom.addVertex(Vector3(0, -height/2, -0.01))
# geom.addColor(Color(0,0,0,0))
# v3 = geom.addVertex(Vector3(width, height/2, -0.01))
# geom.addColor(Color(1,1,0,0))
# v4 = geom.addVertex(Vector3(width, -height/2, -0.01))
# geom.addColor(Color(1,0,0,0))
# geom.addPrimitive(PrimitiveType.TriangleStrip, 0, 4)
# getSceneManager().addModel(geom)

# for h in xrange(0, 9):
	# for v in xrange(0, 8):
		# sphere = StaticObject.create('stellar')
		# sphere.setSelectable(True)
		# targetList.append(sphere)
		# sphere.setPosition(Vector3(-0.5, 0, 0.01))
		# hLoc = h + 0.5
		# degreeConvert = 36.0/360.0*2*pi #18 degrees per panel times 2 panels per viz = 36
		# caveRadius = 3.25
		# screenCenter = SceneNode.create(str(v)+str(h))
		# screenCenter.setPosition(Vector3(sin(hLoc*degreeConvert)*caveRadius, v * 0.29 + 0.41, cos(hLoc*degreeConvert)*caveRadius))
		# screenCenter.yaw(hLoc*degreeConvert + radians(180))
		# screenCenter.addChild(sphere)
		# cam.addChild(screenCenter)