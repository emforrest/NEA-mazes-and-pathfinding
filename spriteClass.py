class Sprite():
    '''The sprite that the user navigates through the maze'''

    def __init__(self):
        self._xy = (0, 0)
        self._cell = () #the cell the sprite is currently on
    #endsub

    def getxy(self):
        return self._xy
    #endsub

    def setxy(self, new):
        self._xy = new
    #endsub

    def getCell(self, cellsList, allCells):
        '''Find the Cell object the sprite is on based on its coordinates'''
        cellPosition = cellsList.index([self._xy[0], self._xy[1]])
        return allCells[cellPosition] 
    #endsub

    def canMove(self, direction, cellsList, allCells):
        '''Test whether the sprite can move in a given direction'''
        move = False
        if direction == 'up':
            movement = (0, -1)
        elif direction == 'down':
            movement = (0, 1)
        elif direction == 'left':
            movement = (-1, 0)
        elif direction == 'right':
            movement = (1, 0)
        #endif

        currentCell = self._xy
        newCell = (currentCell[0] + movement[0], currentCell[1] + movement[1]) #adds the direction to the current cell coordinates
        newPassage = (currentCell, newCell)
        self._cell = self.getCell(cellsList, allCells)
        if newPassage in self._cell.getPassages():
            move = True
        #endif
        newPassage = (newCell, currentCell) #the passage is traversable in both directions, but only one will be listed in the cell's list of passages
        if newPassage in self._cell.getPassages():
            move = True
        #endif

        if move == True:
            self._xy = newCell

        return move, movement        
    #endsub

#endclass
