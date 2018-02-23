import numpy
import matplotlib.pylab as plt
class objectOnTable(object):
	def __init__(self, x, y, theta, shape):
		self.x = x
		self.y = x
		self.shape = shape
		self.theta = theta
		self.delGridX, self.delGridY = self.cellsToOccupy()
	def cellsToOccupy(self):
		if self.shape == 'circle':
			delGridX = 3
			delGridY = 3
		elif self.shape == 'rectangle':
			length = 5
			delGridX = length * numpy.cos(self.theta) / 2
			delGridY = length * numpy.sin(self.theta) / 2
		return delGridX, delGridY
def fillGrid(objectList):
	for obj in objectList:

