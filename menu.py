from omega import *
from omegaToolkit import *

mm = MenuManager.createAndInitialize()
appMenu = mm.createMenu("contolPanel")

def changeOrbit(ratio):
	global globalOrbitScale
	globalOrbitScale *= ratio
	setGlobalOrbitScale(globalOrbitScale)
	
def changeRadius(ratio):
	global globalRadiusScale
	globalRadiusScale *= ratio
	setGlobalRadiusScale(globalRadiusScale)
	
def resetView():
	cam = getDefaultCamera()
	cam.setPosition(Vector3( 10, 2, 10 ))
	cam.yaw(radians(45))
	cam.pitch(radians(-10))

appMenu.addButton("OrbitScale +", "changeOrbit(1.5)")
appMenu.addButton("OrbitScale -", "changeOrbit(1.0/1.5)")
appMenu.addButton("RadiusScale +", "changeRadius(1.5)")
appMenu.addButton("RadiusScale -", "changeRadius(1.0/1.5)")

appMenu.addButton("Show Galaxy", "switchSystemInCave(galaxy)")
appMenu.addButton("Reset View", "resetView()")