from omega import *
from cyclops import *
from math import *
from euclid import *

rootNode = SceneNode.create('root')
getDefaultCamera().addChild(rootNode)

for h in xrange(1, 10): # 2, 20
	# leave a 'hole' in the center of the cave to see the far planets through
	if h == 5:
		continue
		#print "yep"
	for v in xrange(0, 8): # 0, 4
		#outlineBox = BoxShape.create(2.0, 0.25, 0.001)
		outlineBox = SphereShape.create(0.125, 4)
		outlineBox.setPosition(Vector3(-0.5, 0, 0.01))
		outlineBox.setEffect('colored -e red')
		hLoc = h + 0.5
		degreeConvert = 36.0/360.0*2*pi #18 degrees per panel times 2 panels per viz = 36
		caveRadius = 3.25
		screenCenter = SceneNode.create(str(h)+str(v))
		screenCenter.setPosition(Vector3(sin(hLoc*degreeConvert)*caveRadius, v * 0.29 + 0.41, cos(hLoc*degreeConvert)*caveRadius))
		screenCenter.yaw(hLoc*degreeConvert)
		screenCenter.addChild(outlineBox)
		rootNode.addChild(screenCenter)