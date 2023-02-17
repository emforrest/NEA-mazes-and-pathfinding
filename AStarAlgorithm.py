#The A* pathfinding algorithm used to find the shortest route from start cell to end cell

from queue import PriorityQueue

def heuristic(currentCell, targetCell):
    '''Calculates the heuristic used to guess the distance to the target cell using Manhattan Distance'''
    currentxy = currentCell.getxy()
    targetxy = targetCell.getxy()
    return (abs(currentxy[0] - targetxy[0]) + abs(currentxy[1] - targetxy[1])) #manhattan distance formula
#endsub

def calculateRoute(cell, cameFrom):
    '''Retrieve the shortest route by tracing back from target cell to start cell'''
    shortestRoute = [cell.getxy()]
    while cameFrom[cell] != None:
        shortestRoute.append(cameFrom[cell].getxy())
        cell = cameFrom[cell]
    #endwhile
    shortestRoute.reverse()#produces the route from start to target

    return shortestRoute 
#endsub
    
def AStar(startCell, targetCell, allWalls, cellsList, allCells, warpOutCell): 
    '''Use the A* algorithm to find the shortest route to the target cell in a grid'''

    frontier = PriorityQueue() #The frontier is a priority queue of cells currently being checked
    frontier.put(startCell.getxy(), 1)
    totalCosts = {} #A dictionary of each cell and its total cost  
    costsFromStart = {} #A dictionary of each cell and its cost from the start cell
    cameFrom = {startCell:None} #A dictionary of cells that have been visited and the cell directly before them
    colourChanges = [] #Records all cells which should have their colour changed, and to what colour, so that they can be updated in A* Simulation only

    currentCell = frontier.get() #In order to sort the frontier, the cells must be in coordinate form, however to get the cell's neighbours it must be in Cell form. The two lines below convert from coordinate form to Cell form.
    position = cellsList.index([currentCell[0], currentCell[1]])
    currentCell = allCells[position]
    
    while currentCell != targetCell and currentCell != -1: #if it is impossible to reach the target the frontier becomes empty, so currentCell is set to -1

        #Calculate the cell's neighbours
        if currentCell.getType() != 'warp in':
            neighbours = currentCell.getNeighbours()
        else:
            neighbours = warpOutCell.getNeighbours()
        #endif

        for neighbour in neighbours: #check each neigbour individually

            #convert the neighbour's coordinates to its corresponding Cell object
            position = cellsList.index([neighbour[0], neighbour[1]])
            neighbour = allCells[position]
            
            if neighbour not in cameFrom: #don't check if this neighbour has already been visited

                #find the possible wall between these cells
                possibleWall = -1
                currentxy = currentCell.getxy()
                neighbourxy = neighbour.getxy()
                direction = (neighbourxy[0]-currentxy[0], neighbourxy[1] - currentxy[1])
                if direction == (1, 0):
                    possibleWall = ((currentxy[0]+0.5, currentxy[1] -0.5), (currentxy[0]+0.5, currentxy[1]+0.5))
                elif direction == (-1, 0):
                    possibleWall = ((currentxy[0]-0.5, currentxy[1] -0.5), (currentxy[0]-0.5, currentxy[1]+0.5))
                elif direction == (0, 1):
                    possibleWall = ((currentxy[0]-0.5, currentxy[1] +0.5), (currentxy[0]+0.5, currentxy[1]+0.5))
                elif direction == (0, -1):
                    possibleWall = ((currentxy[0]-0.5, currentxy[1] -0.5), (currentxy[0]+0.5, currentxy[1]-0.5))
                #endif

                if possibleWall not in allWalls: #test whether this wall is actually present
                    
                    if currentCell == startCell:
                        costSoFar = 1 #the first cell has no previous cell
                    else:
                        costSoFar = costsFromStart[currentCell] + neighbour.getCost() # +5 for puddles, +1 for all other cells
                    #endif

                    #Calculate the total cost using the cost so far and a heuristic to guess the distance to the end cell
                    costToNeighbour = costSoFar + heuristic(neighbour, targetCell)

                    #update each dictionary and frontier
                    if neighbour not in totalCosts or costToNeighbour < totalCosts[neighbour]: #only use this total if it is lower than any previously recorded totals (or it wouldn't be the shortest path)
                        totalCosts[neighbour] = costToNeighbour
                        costsFromStart[neighbour] = costSoFar
                        frontier.put((int(costToNeighbour), neighbour.getxy())) #the cell's cost is used as its priority, so cells with the lowest cost are checked before those with a higher cost.
                        colourChanges.append((neighbour, '#33ccff')) #light blue as the neighbour has been added to the frontier
                        cameFrom[neighbour] = currentCell
                    #endif
                #endif
            #endif
        #endfor

        colourChanges.append((currentCell, '#0000e6')) #dark blue as the current cell has now been visited

        #retrieve the next cell to be checked from the frontier
        if frontier.empty() == False:
            currentCell = (frontier.get())[1]
            position = cellsList.index([currentCell[0], currentCell[1]])
            currentCell = allCells[position]
        else:
            currentCell = -1
        #endif
    #endwhile

    #retrieve the shortest path
    if currentCell != targetCell:
        return -1, colourChanges
    #endif
    return calculateRoute(targetCell, cameFrom), colourChanges
#endsub
            
