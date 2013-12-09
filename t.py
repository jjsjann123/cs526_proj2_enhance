q = { 'name' : 'planetName', 'star' : 'hostName', 'orbit': 'semi-MajorAxis[AU]', 'size': 'pl_rade', 'year': 'orbitPeriod[years]', 'day': 'rotationPeriod[days]', 'obliquity': 'rotationTilt[deg]', 'inclination': 'inclination[deg]' }


'name' : 'planetName'
'star' : 'hostName'
'orbit': 'semi-MajorAxis[AU]'
'size': 'pl_rade'
'year': 'orbitPeriod[years]'
'day': 'rotationPeriod[days]'
'obliquity': 'rotationTilt[deg]'
'inclination': 'inclination[deg]'

name = planet[index['name']]
		phase = 0
		size = planet[index['size']]
		obj = SphereShap.create(size, 4)
		year = planet[index['year']]
		day = planet[index['day']]
		tilt = planet[index['rotationTilt']]
		self.planetObjList.update({ name: [phase, obj, year, day, majorAxis, inclination, eccentricity]})