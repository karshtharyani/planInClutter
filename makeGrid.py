#! /usr/bin/python
import numpy
from itertools import count
import matplotlib.pylab as plt
class objectOnTable(object):
	_ids = count(0)
	def __init__(self, x, y, theta = None, shape = 'circle'):
		self.x = x
		self.y = y
		self.shape = shape
		self.theta = theta
		self.delGridX, self.delGridY = self.cellsToOccupy()
		self.tag =  next(self._ids)
	def cellsToOccupy(self):
		if self.shape == 'circle':
			delGridX = 1.5
			delGridY = 1.5
		elif self.shape == 'rectangle':
			length = 5
			delGridX = length * numpy.cos(self.theta) / 2
			delGridY = length * numpy.sin(self.theta) / 2
		return delGridX, delGridY
	def updatePose(self, newX, newY, newTheta):
		self.x = newX
		self.y = newY
		self.theta = newTheta
		self.delGridX, self.delGridY = self.cellsToOccupy()

class costMap(object):
	def __init__(self, objOnTableList):
		self.worldMap = self.createWorldMap(objOnTableList)
		self.matMap = self.createMatMap(objOnTableList)

	def createWorldMap(self, objOnTableList):
		worldMap = {}
		for i in range(len(objOnTableList)):
			obj = objOnTableList[i]
			worldMap[obj.tag] = (obj.x, obj.y, obj.delGridX, obj.delGridY)
		return worldMap
	def createMatMap(self, objOnTableList):
		# table dimensions in cm 
		tableWidth = 50
		tableHeight = 50

		matMap = numpy.zeros([tableWidth, tableHeight])
		for i in range(len(objOnTableList)):
			obj = objOnTableList[i]
			x, y, delGridX, delGridY = (obj.x, obj.y, obj.delGridX, obj.delGridY)
			delGridX = numpy.ceil(delGridX);
			delGridY = numpy.ceil(delGridY);
		return matMap
		
	def updateWorldMap(self, obj):
		self.worldMap[obj.tag] = (obj.x, obj.y, obj.delGridX, obj.delGridY)
	def visualize(self):
		tagsOnTable = self.worldMap.keys()
		for tag in tagsOnTable:
			x, y, delGridX, delGridY = self.worldMap[tag]

def updateObjectOnTable(tableMap, obj, newX, newY, newTheta):
	obj.updatePose(newX, newY, newTheta)
	tableMap.updateWorldMap(obj)
	tableMap.updateMatMap(obj)

def planToTarget(tableMap, targetObject):
	pass

if __name__=="__main__":
	spam = objectOnTable(0, 3, -numpy.pi/4, shape = 'rectangle')
	soup = objectOnTable(1, 4)
	glass = objectOnTable(3, 5)
	tableMap = costMap([soup, spam, glass])
	print tableMap.worldMap
	tableMap.visualize()

