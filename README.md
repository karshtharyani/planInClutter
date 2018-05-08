# planInClutter
A visualization to load objects on a table, make a cost map, and decide which objects should be moved out of the way

## Classes in `makeGrid.py`

### objectOnTable

This class is responsible for defining the properties of an object which is on the table.

Members of the Class:
    <p> `self.x` - the x coordinate of the object on the table in centimetre</p>
    <p> `self.y` - the y coordinate of the object on the table in centimetre</p>
    <p> `self.theta(default is none)` - the orientation of the object on the table in degrees </p>
    <p> `self.shape` - the shape of the object can take values `circle(default)`, or `rectangle` </p>

Methods of the Class:
    <p> `cellsToOccupy()` - a method to help decide the footprint of the object based on the shape</p>
    <p> `updatePose(self, newX, newY, newTheta)` - a method to help update the new pose of the object in the map</p>
    
Example: To define an instance of this class 
`soup = objectOnTable(10, 30)`
`spam = objectOnTable(40, 10, numpy.pi/2, shape = 'rectangle')`
### costMap

This class is responsible for making the visualizations of the occupancy grid of the table.

Members of the Class:
    <p> `self.worldMap` - a dictionary with the key as the tag of the object and value as the object</p>
Methods of the Class:
    <p> `createWorldMap` - creates the worldMap </p>
    <p> `createMatMap` - creates the matMap </p>
    <p> `updateWorldMap` - updates the worldMap </p>
    <p> `updateMatMap` - updates the matMap </p>
    <p> `visualize` - visualizes the matMap </p>

