#The randomised depth first search algorithm used to create a maze

import random
from cellClasses import Cell, StartCell, EndCell

def depthFirstRecursion(current, allCells, cellsList, totalPassages):
    '''Create a list of passages by using the randomised depth first search algorithm on the grid'''
    current.setVisited(True)
    neighbours = current.getNeighbours()
    random.shuffle(neighbours) #hence the algorithm is randomised so a maze can be created

    for neighbour in neighbours:
        position = cellsList.index(neighbour)
        neighbour = allCells[position] 
        if neighbour.getVisited() == False:

            #add the passage between these cells to each cell's passage list and the list of all passages (forming an adjacency list)
            currentxy = current.getxy()
            neighbourxy = neighbour.getxy()
            passage = (currentxy, neighbourxy) 
            currentPassages = current.getPassages()
            neighbourPassages = neighbour.getPassages()
            currentPassages.append(passage)
            neighbourPassages.append(passage)
            totalPassages.append(passage)

            totalPassages = depthFirstRecursion(neighbour, allCells, cellsList, totalPassages) #the algorithm is then recalled using the neighbour cell. It unwinds once all of a cell's neighbours have already been visited.
        #endif
    #endfor
    return totalPassages
#endsub

def main(size, theme):
    '''Initialise the grid ready to pass into the recursive subroutine'''
    allCells = [] #allCells is a list of Cell objects for each cell in the grid
    cellsList=[] #cellsList is a list of these cells in coordinate form (x, y), preventing multiple instances of the same cell from being created
    for x in range(size):
        for y in range(size):
            cellsList.append ([x, y])
            if x==0 and y==0:
                allCells.append(StartCell(x, y, size, size, theme))
            elif x==size-1 and y==size-1:
                allCells.append(EndCell(x, y, size, size, theme))
            else:
                allCells.append(Cell(x, y, size, size, theme))
            #endif
        #endfor
    #endfor
    current = allCells[0] #the start cell
    totalPassages = []
    totalPassages = depthFirstRecursion(current, allCells, cellsList, totalPassages)
    return(totalPassages, allCells, cellsList)
#endsub

