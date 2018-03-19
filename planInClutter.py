#! /usr/bin/python
from __future__ import division
from makeGrid import *
import matplotlib.pylab as plt
import math
import numpy as np
from collections import namedtuple
import IPython

def planInClutter(tableMap, targetObject):
	tableMap.visualize()
	obstacles = obstaclesInWay(targetObject.tag, tableMap) 
	print "these tags are obstacles :", obstacles
	tableMap.visualize()
	obstacleTags = {}
	for tag in obstacles:
		objObstacle = tableMap.worldMap[tag]
		rObjObs, thetaObjObs = convertObjectToPolar(objObstacle)
		obstacleTags[rObjObs] = tag
		
	for rNearest in sorted(obstacleTags.keys()):
		tag = obstacleTags[rNearest]
		newX, newY, newTheta = findOpenSpot(tag, tableMap)
		print newX, newY, newTheta
		updateObjectOnTable(tableMap, tableMap.worldMap[tag], newX, newY, newTheta)
		tableMap.visualize()
	
def updateObjectOnTable(tableMap, obj, newX, newY, newTheta):
	obj.updatePose(newX, newY, newTheta)
	tableMap.updateWorldMap(obj)

def convertObjectToPolar(tableObject):
	xTarget = tableObject.x
	yTarget = tableObject.y
	rTarget = math.sqrt(xTarget**2 + yTarget**2)
	thetaTarget = math.atan(xTarget/yTarget) * 180 / math.pi
	return rTarget, thetaTarget

def isObstacle(rTarget, thetaTarget, rObj, thetaObj, thetaTolerance):
	thetaUpper = thetaTarget + thetaTolerance	
	thetaLower = thetaTarget - thetaTolerance	
	if rObj < rTarget and thetaObj > thetaLower and thetaObj < thetaUpper:
		return True
def findOpenSpot(tag, tableMap):
	obj = tableMap.worldMap[tag]
	filterSize = namedtuple('filterSize', ['r', 'c'], verbose = False)
	filtersz = filterSize(int(2 * numpy.ceil(obj.delGridX)), int(2 * numpy.ceil(obj.delGridY)))
	initialX = int(numpy.ceil(obj.x))
	newX, newY = convolve(tableMap.matMap, filtersz, initialX)
	return newX, newY, numpy.pi/2
	
def convolve(matMap, filtersz, initialX):
	outOfBounds = 0
	newX = 0
	newY = 0
	for i in range(initialX, numpy.size(matMap, 0)):
		for j in range(2, numpy.size(matMap, 1)):
			rCorn1 = i - int(filtersz[0] / 2)
			rCorn2 = i + int(filtersz[0] / 2) + 1
			cCorn1 = j - int(filtersz[1] / 2)
			cCorn2 = j + int(filtersz[1] / 2) + 1
			print "Corner 1: "
			print (rCorn1, cCorn1)
			print "Corner 2: "
			print (rCorn2, cCorn2)
			roi = matMap[rCorn1:rCorn2, cCorn1:cCorn2];
			print roi
			print 
			roiTruth = roi >= 0
			if roiTruth.all() == True:
				newX = i
				newY = j
				return newX, newY

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
					matMap[j, i] = -0.5
					matMap[j1, i] = -0.5
				except:
					print "index not possible"

def obstaclesInWay(tagTarget, tableMap, thetaTolerance = 15):
	targetObject = tableMap.worldMap[tagTarget]
	rTarget, thetaTarget = convertObjectToPolar(targetObject)
	thetaUpper = thetaTarget + thetaTolerance	
	thetaLower = thetaTarget - thetaTolerance	
	obstacles = []
	matrixWorld = tableMap.matMap
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
	soup = objectOnTable(20, 20)
	soup1 = objectOnTable(10, 10)
	soup2 = objectOnTable(15, 10)
	spam = objectOnTable(20, 10, numpy.pi/2, shape = 'rectangle')
	glass = objectOnTable(30, 20)
	tableMap = costMap([soup, soup1, soup2, spam, glass])
	planInClutter(tableMap, glass)
			
