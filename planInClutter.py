#! /usr/bin/python
from __future__ import division
from makeGrid import *
import math

def planInClutter(tableMap, targetObject):
	pass
	
def updateObjectOnTable(tableMap, obj, newX, newY, newTheta):
	obj.updatePose(newX, newY, newTheta)
	tableMap.updateWorldMap(obj)

def obstaclesInWay(tagTarget, tableMap, thetaTolerance = 10):
	targetObject = tableMap.worldMap[tagTarget]
	xTarget = targetObject[0]
	yTarget = targetObject[1]
	rTarget = math.sqrt(targetObject[0]**2 + targetObject[1]**2)
	thetaTarget = math.atan(xTarget/yTarget) * 180 / math.pi

if __name__ == "__main__":
	soup = objectOnTable(30, 40)
	soup1 = objectOnTable(10, 20)
	soup2 = objectOnTable(30, 25)
	spam = objectOnTable(40, 20, numpy.pi/2, shape = 'rectangle')
	glass = objectOnTable(20, 30)
	tableMap = costMap([soup, soup1, soup2, spam, glass])
	obstaclesInWay(0, tableMap) 
			
