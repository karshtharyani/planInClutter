#! /usr/bin/python
from __future__ import division
from makeGrid import *
import matplotlib.pylab as plt
import math
import numpy as np

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
def findOpenSpot(tag, tableMap):
	pass
	
def fillGridRegion(matMap, rTarget, thetaUpper, thetaLower):
	thetaUpper = int(math.floor(thetaUpper))
	thetaLower = int(math.floor(thetaLower))
	for theta in range(thetaLower, thetaUpper):
		theta = theta * math.pi / 180
		for i in range(0,50):
			j = int(math.ceil(math.tan(theta) * i))
			j1 = int(math.floor(math.tan(theta) * i))
			if i**2 + j**2 <= rTarget**2:
				try:
					matMap[j, i] = -2
					matMap[j1, i] = -2
				except:
					print "index not possible"

def obstaclesInWay(tagTarget, tableMap, thetaTolerance = 10):
	targetObject = tableMap.worldMap[tagTarget]
	rTarget, thetaTarget = convertObjectToPolar(targetObject)
	thetaUpper = thetaTarget + thetaTolerance	
	thetaLower = thetaTarget - thetaTolerance	
	obstacles = []
	matrixWorld = tableMap.matMap
	print "rTarget", rTarget
	fillGridRegion(matrixWorld, rTarget, thetaUpper, thetaLower)

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
	spam = objectOnTable(20, 40, numpy.pi/2, shape = 'rectangle')
	glass = objectOnTable(35, 25)
	tableMap = costMap([soup, soup1, soup2, spam, glass])
	tableMap.visualize()
	obstacles = obstaclesInWay(2, tableMap) 
	print "these tags are obstacles :", obstacles
	tableMap.visualize()
			
