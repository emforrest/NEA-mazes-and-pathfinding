#The Cell class, from which grids can be created, and its subclasses, different objects for the A* section.

from tkinter import PhotoImage

class Cell:

    def __init__(self, x, y, height, width, theme):
        self.__xy = (x, y)
        self._visited = False
        self.__neighbours = self.__calculateNeighbours(height, width)
        self.__edges = self.__calculateEdges()
        self._passages = []  #used when checking if the sprite can move here in Maze Game
        self._colour = theme['background']
        self._type = 'empty' #determines which kind of cell a particular Cell object is
        self._cost = 1 #cost to cross this cell
    #endsub
    
    def getxy(self):
        return self.__xy
    #endsub
    
    def getVisited(self):
        return self._visited
    #endsub

    def setVisited(self, new):
        self._visited = new
    #endsub

    def getNeighbours(self):
        return self.__neighbours
    #endsub

    def getEdges(self):
        return self.__edges
    #endsub

    def getPassages(self):
        return self._passages
    #endsub
    
    def getColour(self):
        return self._colour
    #endsub

    def setColour(self, new):
        self._colour = new
    #endsub

    def getType(self):
        return self._type
    #endsub

    def getCost(self):
        return self._cost
    #endsub

    def __calculateNeighbours(self, height, width):
        '''Given a cell's coordinates, return a list of its neighbouring cells'''
        directions = [[0,1], [1,0], [0,-1], [-1,0]]
        neighbours = []
        for d in directions:
            neighbour = [self.__xy[0] + d[0], self.__xy[1] +d[1]] 
            if -1<neighbour[0] <width and -1<neighbour[1]<height:
                neighbours.append(neighbour) #only add the neighbour if it falls inside the grid.
            #endif
        #endfor
        return neighbours
    #endsub

    def __calculateEdges(self):
        '''Calculate the coordinates of the four edges of this cell'''
        edge1 = ((self.__xy[0]-0.5, self.__xy[1]-0.5), (self.__xy[0]+0.5, self.__xy[1]-0.5))
        edge2 = ((self.__xy[0]-0.5, self.__xy[1]-0.5), (self.__xy[0]-0.5, self.__xy[1]+0.5))
        edge3 = ((self.__xy[0]+0.5, self.__xy[1]-0.5), (self.__xy[0]+0.5, self.__xy[1]+0.5))
        edge4 = ((self.__xy[0]-0.5, self.__xy[1]+0.5), (self.__xy[0]+0.5, self.__xy[1]+0.5))
        edges = [edge1, edge2, edge3, edge4]
        return edges
    #endsub

#endclass

class StartCell(Cell):

    def __init__(self, x, y, height, width, theme):
        super().__init__(x, y, height, width, theme)
        self._type = 'start'
        self._colour = PhotoImage(file = 'startcell.png')
    #endsub

#endclass

class EndCell(Cell):

    def __init__(self, x, y, height, width, theme):
        super().__init__(x, y, height, width, theme)
        self._type = 'end'
        self._colour = PhotoImage(file = 'endcell.png')
    #endsub

#endclass

class Wall(Cell):

    def __init__(self, x, y, height, width, theme):
        super().__init__(x, y, height, width, theme)
        self._type = 'wall'
        self._colour = '#000000'
    #endsub

#endclass

class Puddle(Cell):

    def __init__(self, x, y, height, width, theme):
        super().__init__(x, y, height, width, theme)
        self._type = 'puddle'
        self._colour = PhotoImage(file = 'puddle.png')
        self._cost = 5
    #endsub
    
#endclass

class WarpIn(Cell):

    def __init__(self, x, y, height, width, theme):
        super().__init__(x, y, height, width, theme)
        self._type = 'warp in'
        self._colour = PhotoImage(file = 'warpin.png')
    #endsub
        
#endclass

class WarpOut(Cell):

    def __init__(self, x, y, height, width, theme):
        super().__init__(x, y, height, width, theme)
        self._type = 'warp out'
        self._colour = PhotoImage(file = 'warpout.png')
    #endsub

#endclass
