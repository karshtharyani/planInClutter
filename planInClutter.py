#! /usr/bin/python
from __future__ import division
from makeGrid import *
import matplotlib.pylab as plt
import math

def planInClutter(tableMap, targetObject):
	pass
	
def updateObjectOnTable(tableMap, obj, newX, newY, newTheta):
	obj.updatePose(newX, newY, newTheta)
	tableMap.updateWorldMap(obj)

def convertObjectToPolar(tableObject):
	xTarget = tableObject[0]
	yTarget = tableObject[1]
	rTarget = math.sqrt(tableObject[0]**2 + tableObject[1]**2)
	thetaTarget = math.atan(xTarget/yTarget) * 180 / math.pi
	return rTarget, thetaTarget

def isObstacle(rTarget, thetaTarget, rObj, thetaObj, thetaTolerance):
	thetaUpper = thetaTarget + thetaTolerance	
	thetaLower = thetaTarget - thetaTolerance	
	if rObj < rTarget and thetaObj > thetaLower and thetaObj < thetaUpper:
		return True
	

def obstaclesInWay(tagTarget, tableMap, thetaTolerance = 10):
	targetObject = tableMap.worldMap[tagTarget]
	rTarget, thetaTarget = convertObjectToPolar(targetObject)
	obstacles = []
	for tag in tableMap.worldMap.keys():
		if tag == tagTarget:
			continue
		tableObj = tableMap.worldMap[tag]
		rObj, thetaObj = convertObjectToPolar(tableObj)
		if isObstacle(rTarget, thetaTarget, rObj, thetaObj, thetaTolerance):
			obstacles.append(tag)
	return obstacles

if __name__ == "__main__":
	soup = objectOnTable(10, 10)
	soup1 = objectOnTable(15, 20)
	soup2 = objectOnTable(30, 35)
	spam = objectOnTable(40, 40, numpy.pi/2, shape = 'rectangle')
	glass = objectOnTable(35, 25)
	tableMap = costMap([soup, soup1, soup2, spam, glass])
	obstaclesInWay(2, tableMap) 
	tableMap.visualize()
			
