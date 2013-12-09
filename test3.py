from xmlReader import *

def pp(target):
	print target['stellar']
	print target['star']
	for q in target['planets']:
		#print target['planets'][q]
		print q

systemDir = "./stellar/"

q = readAllFilesInDir(systemDir)

print " system without distance "
for t in q:
    if q[t]['stellar']['distance'] == 1:
            print q[t]['stellar']['name']

print " system without temperature "
for t in q:
    if q[t]['star'][0]['temperature'] == None:
            print q[t]['stellar']['name']

print "system without type"
starType = {}
for t in q:
	type = q[t]['star'][0]['spectraltype']
	if type != None:
		starType.update({type:0})
	else:
		print q[t]['stellar']['name']
		
print "system without radius"
starRadius = []
for t in q:
	type = q[t]['star'][0]['radius']
	if type != None:
		starRadius.append(type)
	else:
		print q[t]['star']['radius']