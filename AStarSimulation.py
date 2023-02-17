#The main part of A* Simulation

from math import floor
import tkinter
from tkinter import messagebox
from cellClasses import Cell, StartCell, EndCell, Wall, Puddle, WarpIn, WarpOut
from AStarAlgorithm import AStar

#Objects

class AStarClass():
    '''This class contains all the variables required across different subroutines. This is because subroutines called using a button cannot return a variable.'''

    def __init__(self):
        self.__HEIGHT = 10
        self.__WIDTH = 24
        self._currentObject = 'wall'
        self.__SCALE = 47
        self.__TRANSLATE = 25 #these constants are used to scale and translate the grid to the correct proportion
        self._cellsList = []
        self._allCells = []
        self._walls = [] #a list of walls (the sides of each Wall cell placed on the grid)
        self._gridArea = None
        self._images = [] #a list of images to be displayed on the grid so they don't get garbage collected
        self._editGrid = True
        self._returnToMenu = False
        self._infoPage = None
        self._portalPage = None
    #endsub

    def getHeight(self):
        return self.__HEIGHT
    #endsub

    def getWidth(self):
        return self.__WIDTH
    #endsub

    def getCurrentObject(self):
        return self._currentObject
    #endsub

    def setCurrentObject(self, new): 
        self._currentObject = new
    #endsub

    def getScale(self):
        return self.__SCALE
    #endsub

    def getTranslate(self):
        return self.__TRANSLATE
    #endsub

    def getCellsList(self):
        return self._cellsList
    #endsub

    def setCellsList(self, new): 
        self._cellsList = new
    #endsub

    def getAllCells(self):
        return self._allCells
    #endsub

    def setAllCells(self, new): 
        self._allCells = new
    #endsub

    def getWalls(self):
        return self._walls
    #endsub

    def setWalls(self, new): 
        self._walls = new
    #endsub

    def getGridArea(self):
        return self._gridArea
    #endsub

    def setGridArea(self, new): 
        self._gridArea = new
    #endsub

    def getImages(self):
        return self._images
    #endsub

    def setImages(self, new): 
        self._images = new
    #endsub

    def getEditGrid(self):
        return self._editGrid
    #endsub

    def setEditGrid(self, new): 
        self._editGrid = new
    #endsub

    def getReturnToMenu(self):
        return self._returnToMenu
    #endsub

    def setReturnToMenu(self, new): 
        self._returnToMenu = new
    #endsub

    def getInfoPage(self):
        return self._infoPage
    #endsub

    def setInfoPage(self, new): 
        self._infoPage = new
    #endsub

    def getPortalPage(self):
        return self._portalPage
    #endsub

    def setPortalPage(self, new): 
        self._portalPage = new
    #endsub

#endclass

#Displaying information

def closePortalPage(variables):
    '''Properly close the information window'''
    variables.getPortalPage().destroy()
    variables.setPortalPage(None)
#endsub

def portalPage(variables):
    '''Display a page explaining why portals may not be discovered.'''
    if variables.getPortalPage():
        variables.getPortalPage().destroy()
    #endsub   

    portalWindow = tkinter.Tk()
    portalWindow.title('Maze-solving using A*')
    portalWindow.geometry('900x600')
    portalWindow.configure(bg = '#ffffff')
    portalWindow.protocol('WM_DELETE_WINDOW', lambda: closePortalPage(variables))

    title = tkinter.Label(portalWindow, text = 'The Portal Problem', font = '"OCR A Extended" 20 ', fg = '#0015d4', bg = '#ffffff')
    title.place(relx = 0.05, rely = 0.05)

    text1 = tkinter.Text(portalWindow, font = 'Verdana 15', fg = '#000000', bg = '#ffffff', height = 100, width = 63, wrap = 'word', bd = 0)
    text1.insert('insert', 'Portals allow the algorithm to \'jump\' between two locations in the grid. This can save loads of time that would be needed to cross those cells normally. Super useful, right?\n\nWell, only if you make it so. You could position the portal out nowhere near the target, making it a complete waste. How evil.\n\nThe problem with portals is that the A* algorithm only considers distance from the start and target cell. It wasn\'t designed to know about portals. The result of this, is that if the algorithm wouldn\'t have visited the portal in if it were a normal cell, it won\'t visit it. Even if the portal out is right next to the target cell. The algorithm doesn\'t check for portals at all, only using them if it manages to stumble across the portal in.\n\nThe downside of this is that occasionally, a maze is created where taking the portal would be much faster than the route found by the algorithm, however the algorithm didn\'t spot it. Why don\'t you try to create a situation like this?')
    text1.config(state = 'disabled')

    text1.tag_add('algorithm', 5.37, 5.104)
    text1.tag_configure('algorithm', font = 'Verdana 15 bold')

    text1.tag_add('no visit', 5.257, 5.272)
    text1.tag_configure('no visit', font = 'Verdana 15 bold')

    text1.place(relx = 0.05, rely = 0.12)

    backButton = tkinter.Button(portalWindow, text = 'Back', font = '"OCR A Extended" 15', fg = '#000000', bg = '#e2e2e2', activebackground = '#cccccc', relief = 'raised', padx = 2, pady = 2, bd = 4, command = lambda:closePortalPage(variables))
    backButton.place(relx = 0.87, rely = 0.87)

    variables.setPortalPage(portalWindow)

    portalWindow.mainloop()
#endsub

def closeInfoPage(variables):
    '''Properly close the information window'''
    variables.getInfoPage().destroy()
    variables.setInfoPage(None)
#endsub

def infoPage(variables):
    '''Display a page giving information on what the algoithm is and how it works'''

    if variables.getInfoPage():
        variables.getInfoPage().destroy()
    #endsub          

    infoWindow = tkinter.Tk()
    infoWindow.title('Maze-solving using A*')
    infoWindow.geometry('1200x800')
    infoWindow.configure(bg = '#ffffff')
    infoWindow.protocol('WM_DELETE_WINDOW', lambda: closeInfoPage(variables))

    title1 = tkinter.Label(infoWindow, text = 'What\'s going on?', font = '"OCR A Extended" 20 ', fg = '#0015d4', bg = '#ffffff')
    title1.place(relx = 0.03, rely = 0.03)

    title2 = tkinter.Label(infoWindow, text = 'How does it work?', font = '"OCR A Extended" 20 ', fg = '#0015d4', bg = '#ffffff')
    title2.place(relx = 0.43, rely = 0.03)

    text1 = tkinter.Text(infoWindow, font = '"Verdana" 15', fg = '#000000', bg = '#ffffff', height = 100, width = 30, wrap = 'word', bd = 0)
    text1.insert(tkinter.INSERT, 'This page allows you to explore the A* pathfinding algorithm – a method of finding the shortest path between two cells. You can add objects to the grid by clicking their icon, then clicking on a cell in the grid. Click again to remove it.\n\n - Add a start and target cell, then watch the algorithm calculate the shortest route between them.\n\n - Walls are uncrossable – the algorithm will have to find its way around them. Try making a maze!\n\n - Puddles take longer to cross than empty cells. Is it faster to just go around?\n\n - Portals allow you to warp across the grid, from the portal in to the portal out.\n\nWhen you’re happy with your maze, hit ‘Run A*’ to see the algorithm find the optimal solution.')
    text1.config(state='disabled')

    #colour certain words
    text1.tag_add('start', 3.8, 3.14)
    text1.tag_configure('start', foreground = '#00ee00')

    text1.tag_add('target', 3.18, 3.25)
    text1.tag_configure('target', foreground = '#ee0000')

    text1.tag_add('walls', 5.3, 5.8)
    text1.tag_configure('walls', foreground = '#505050')

    text1.tag_add('puddles', 7.3, 7.11)
    text1.tag_configure('puddles', foreground = '#663300')

    text1.tag_add('portals', 9.3, 9.11)
    text1.tag_configure('portals', foreground = '#b800e6')

    text1.tag_add('portal in', 9.54, 9.64)
    text1.tag_configure('portal in', foreground = '#cc99ff')

    text1.tag_add('portal in', 9.54, 9.64)
    text1.tag_configure('portal in', foreground = '#cc99ff')

    text1.tag_add('portal out', 9.72, 9.82)
    text1.tag_configure('portal out', foreground = '#6600cc')

    text1.tag_add('run a*', 11.39, 11.45)
    text1.tag_configure('run a*', foreground = '#1aff9c')
    
    text1.place(relx = 0.03, rely = 0.08)

    line = tkinter.Canvas(infoWindow, bg = '#000000', height = 750, width = 2)
    line.place(relx = 0.4, rely = 0.03)

    text2 = tkinter.Text(infoWindow, font = '"Verdana" 15', fg = '#000000', bg = '#ffffff', height = 100, width = 50, wrap = 'word', bd = 0)
    text2.insert('insert', 'Beginning at the start cell, the algorithm calculates a total cost to travel to each of the cell’s neighbours. This cost is as follows:\n\n\n\n\n\n\nThe distance to the end cell is an estimate as there may be walls in the way. These neighbour cells are added to the frontier – a list of cells with a calculated cost that haven\'t been visited, indicated in light blue. Also, the cell that came before them (in this case, the start cell) is recorded. Next, the cell in the frontier with the lowest cost is picked from the frontier, so the algorithm prioritises directions with a lower cost. This cell’s own neighbours then have a cost calculated and are added to the frontier, and the cell itself is marked as visited – shown in dark blue. \n\nThese steps are repeated until the target cell is reached. The algorithm then checks which cell came before the target, then which cell came before that cell, and so on until the start cell is reached. These are the cells that are part of the shortest route, which is illustrated in yellow.')
    text2.config(state = 'disabled')

    text2.tag_add('light blue', 8.207, 8.217)
    text2.tag_configure('light blue', foreground = '#33ccff')

    text2.tag_add('dark blue', 8.578, 8.587)
    text2.tag_configure('dark blue', foreground = '#0000e6')

    text2.tag_add('yellow', 10.282, 10.289)
    text2.tag_configure('yellow', foreground = '#ffff00')

    text2.place(relx = 0.43, rely = 0.08)

    text3 = tkinter.Label(infoWindow, text = 'Total cost to cell\n=\nTotal distance from start cell\n+\nEstimated total distance to end cell', font = '"Consolas" 15', fg = '#000000', bg = '#9999ff', bd = 0, justify = 'center')
    text3.place(relx = 0.5, rely = 0.17)

    portalButton = tkinter.Button(infoWindow, text = 'The Portal Problem', font = '"OCR A Extended" 15', fg = '#000000', bg = '#e2e2e2', activebackground = '#cccccc', relief = 'raised', padx = 2, pady = 2, bd = 4, command = lambda: portalPage(variables))
    portalButton.place(relx = 0.43, rely = 0.9)

    backButton = tkinter.Button(infoWindow, text = 'Back', font = '"OCR A Extended" 15', fg = '#000000', bg = '#e2e2e2', activebackground = '#cccccc', relief = 'raised', padx = 2, pady = 2, bd = 4, command = lambda:closeInfoPage(variables))
    backButton.place(relx = 0.9, rely = 0.9)

    variables.setInfoPage(infoWindow)

    infoWindow.mainloop()
#endsub

#Clearing the grid

def clearGrid(variables):
    '''Clear the canvas so the user can start over'''

    if variables.getEditGrid() == True:
        allCells = variables.getAllCells()
        for cell in allCells:
            oldColour = cell.getColour() #colour is used to reset blue and yellow cells as well as non-empty cells
            if oldColour != '#f0f0f0':

                #replace the cell instance with that of an empty cell
                xy = cell.getxy()
                allCells.remove(cell)
                del cell
                position = variables.getCellsList().index([xy[0], xy[1]])
                cell = Cell(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})
                allCells.insert(position, cell)
                variables.setAllCells(allCells)

                drawCell(cell, variables) #redraw the empty cell
            #endif
        #endfor
    #endif
    variables.setWalls([]) #remove all walls 
#endsub          
           
#Creating the grid

def drawCell(cell, variables):
    '''Given a cell, draw it to the grid'''
    xy = cell.getxy()
    topleft = (xy[0] -0.5, xy[1] -0.5)
    bottomright = (xy[0]+0.5, xy[1]+0.5)
    colour = cell.getColour()
    gridArea = variables.getGridArea()
    images = variables.getImages()

    if type(colour) == str:
        gridArea.create_rectangle(topleft[0]*variables.getScale()+variables.getTranslate(), topleft[1]*variables.getScale()+variables.getTranslate(), bottomright[0]*variables.getScale()+variables.getTranslate(), bottomright[1]*variables.getScale()+variables.getTranslate(), fill = cell.getColour(), outline = '#000000')
    else:
        colour = colour.zoom(3, 3)
        colour = colour.subsample(2, 2)
        position = variables.getAllCells().index(cell)
        images[position] = colour
        gridArea.create_image(topleft[0]*variables.getScale()+variables.getTranslate(), topleft[1]*variables.getScale()+variables.getTranslate(), image = images[position], anchor = 'nw')
    #endif

    variables.setGridArea(gridArea)
    variables.setImages(images)
#endsub

def addObject(event, variables):
    '''Add the selected cell type to the grid'''

    if variables.getEditGrid() == True: #don't make changes while the algorithm is running

        #Find the position of the mouse
        mousex = int(event.x)
        mousey = int(event.y)
        mousex /= variables.getScale() #Descale these coordinates so they fit within a cell
        mousey /= variables.getScale()
        cellx = floor(mousex) #get the integer value
        celly = floor(mousey)
        if cellx <=23 and celly <= 9:
            cellPosition = variables.getCellsList().index([cellx, celly]) #Find the corresponding Cell object
            cell = variables.getAllCells()[cellPosition]

            #Replace this cell with one of the chosen type
            oldType = cell.getType()
            xy = cell.getxy()
            allCells = variables.getAllCells()
            position = allCells.index(cell)
            allCells.remove(cell)
            del cell

            walls = variables.getWalls()
            images = variables.getImages()

            newCell = Cell(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'}) #the default is an empty cell

            #Remove the walls if appropriate
            if oldType == 'wall':
                walls.remove(newCell.getEdges()[0])
                walls.remove(newCell.getEdges()[1])
                walls.remove(newCell.getEdges()[2])
                walls.remove(newCell.getEdges()[3])
            #endif

            if oldType == variables.getCurrentObject():
                images[position] = '' #reset the image at this position to empty
                newCell = Cell(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})
            else:
                #first reset the cell's colour
                drawCell(newCell, variables)

                if variables.getCurrentObject() == 'wall':
                    newCell = Wall(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})
                    #add a wall for each side of this cell
                    walls.append(newCell.getEdges()[0])
                    walls.append(newCell.getEdges()[1])
                    walls.append(newCell.getEdges()[2])
                    walls.append(newCell.getEdges()[3])

                elif variables.getCurrentObject() == 'start':
                    found, c = alreadyPlaced('start', variables)
                    if found == False: #there can only be one start cell
                        newCell = StartCell(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})
                    else:
                        messagebox.showwarning(title = 'Maze solving using A*', message = 'You can only place one start cell.')
                    #endif

                elif variables.getCurrentObject() == 'end':
                    found, c = alreadyPlaced('end', variables)
                    if found == False:
                        newCell = EndCell(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})
                    else:
                        messagebox.showwarning(title = 'Maze solving using A*', message = 'You can only place one target cell.')
                    #endif

                elif variables.getCurrentObject() == 'puddle':
                    newCell = Puddle(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})

                elif variables.getCurrentObject() == 'warp in':
                    found, c = alreadyPlaced('warp in', variables)
                    if found == False:
                        newCell = WarpIn(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})
                    else:
                        messagebox.showwarning(title = 'Maze solving using A*', message = 'There can only be one portal system.')
                    #endif

                elif variables.getCurrentObject() == 'warp out':
                    found, c = alreadyPlaced('warp out', variables)
                    if found == False: 
                        newCell = WarpOut(xy[0], xy[1], variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'})
                    else:
                        messagebox.showwarning(title = 'Maze solving using A*', message = 'There can only be one portal system.')
                    #endif
                #endif
            #endif

            allCells.insert(cellPosition, newCell)
            variables.setAllCells(allCells)
            variables.setImages(images)
            variables.setWalls(walls)
            drawCell(newCell, variables) #display the new cell on screen
        #endif
    #endif
#endsub

#Checking the grid is valid

def alreadyPlaced(desiredType, variables):
    '''Check whether a certain type of cell has been placed on the grid and return it, using a linear search'''
    found = False
    for cell in variables.getAllCells():
        if cell.getType() == desiredType:
            found = True
            return found, cell #the loop ends as the cell was found
        #endif
    #endfor
    return found, -1
#endsub

def checkGrid(variables, AStarWindow):
    '''Check that the user's grid is valid (has a start and end cell and both or no portals)'''
    
    variables.setEditGrid(False) #so the user cannot make changes while the algorithm is running
    startPresent, startCell = alreadyPlaced('start', variables)
    endPresent, endCell = alreadyPlaced('end', variables)
    warpInPresent, warpInCell = alreadyPlaced('warp in', variables)
    warpOutPresent, warpOutCell = alreadyPlaced('warp out', variables)

    #produce an error message if the grid is invalid
    if startPresent == False:
        messagebox.showwarning(title = 'Maze solving using A*', message = 'The grid is missing a start cell.')
    elif endPresent == False:
        messagebox.showwarning(title = 'Maze solving using A*', message = 'The grid is missing a target cell.')
    elif warpInPresent == True and warpOutPresent == False:
        messagebox.showwarning(title = 'Maze solving using A*', message = 'The portal needs an exit.')
    elif warpInPresent == False and warpOutPresent == True:
        messagebox.showwarning(title = 'Maze solving using A*', message = 'The portal needs an entrance.')
    else:
        runAStar(variables, startCell, endCell, warpOutCell, AStarWindow)
    #endif
    variables.setEditGrid(True)
#endsub  

#Running the A* algorithm

def wait(AStarWindow):
    '''Used to add a break between displaying changes to the frontier'''
    var = tkinter.IntVar()
    AStarWindow.after(50, var.set, 1)
    AStarWindow.wait_variable(var)
#endsub

def runAStar(variables, startCell, endCell, warpOutCell, AStarWindow):
    '''Use the A* algorithm to find the solution, and display it on the grid.'''

    #Reset cells whose colour was changed in a previous run
    for cell in variables.getAllCells():
        oldColour = cell.getColour()
        if oldColour != '#f0f0f0':
            cell.setColour('#f0f0f0')
            drawCell(cell, variables)
            if cell.getType() != 'empty': #redraw the sprite on top of the blank square if the cell was not empty
                cell.setColour(oldColour)
                drawCell(cell, variables)  
            #endif
        #endif
    #endfor

    #Calculate the fastest route through the grid
    shortestRoute, colourChanges = AStar(startCell, endCell, variables.getWalls(), variables.getCellsList(), variables.getAllCells(), warpOutCell)

    #Change each cell's colour as specified in the AStar subroutine
    for change in colourChanges: #change is in the form (cell, colour)
        cell = change[0]
        oldColour = cell.getColour()
        cell.setColour(change[1])
        drawCell(cell, variables)
        if cell.getType() != 'empty': #redraw the object on top of the new colour
            cell.setColour(oldColour)
            drawCell(cell, variables)
        #endif
        wait(AStarWindow)
    #endfor

    #Draw the solution in yellow
    if shortestRoute != -1: #if the algorithm did not fail
        for cell in shortestRoute:
            position = variables.getCellsList().index([cell[0], cell[1]])
            cell = variables.getAllCells()[position]
            if cell.getType() == 'empty':
                cell.setColour('#ffff00')
                drawCell(cell, variables)
            else:
                oldImage = cell.getColour()
                cell.setColour('#ffff00')
                drawCell(cell, variables)
                cell.setColour(oldImage)
                drawCell(cell, variables)
            #endif

            #change the colour of the portal out if part of the fastest route (as it isn't in solution) 
            if cell.getType() == 'warp in':
                oldImage = warpOutCell.getColour()
                warpOutCell.setColour('#ffff00')
                drawCell(warpOutCell, variables)
                warpOutCell.setColour(oldImage)
                drawCell(warpOutCell, variables)
            #endif
                
            wait(AStarWindow)
        #endfor
    #endif
#endsub  

#Exiting A* Section

def returnToMenu(window, variables):
    if variables.getEditGrid() == True:
        window.destroy()
        variables.setReturnToMenu(True)
    #endif
#endsub

#Main window

def closeWindows(AStarWindow, variables):
    '''Close the information or portal problem window if the user closes the main window'''
    AStarWindow.destroy()
    if variables.getInfoPage():
        variables.getInfoPage().destroy()
    #endif
    if variables.getPortalPage():
        variables.getPortalPage().destroy()
    #endif
#endsub

def main(variables):
    '''The main subroutine for A* Simulation, used to display the page and handle user input'''

    #Produce the background window
    AStarWindow = tkinter.Tk()
    AStarWindow.title('Maze-solving using A*')
    AStarWindow.geometry('1200x700')
    AStarWindow.configure(bg = '#ffffff')
    AStarWindow.protocol('WM_DELETE_WINDOW', lambda: closeWindows(AStarWindow, variables))

    title = tkinter.Label(AStarWindow, text = 'A* Pathfinding Visualisation', font = '"OCR A Extended" 22 underline', fg = '#000000', bg = '#ffffff')
    title.place(relx = 0.28, rely = 0.015)

    gridArea = tkinter.Canvas(AStarWindow, bd = 0, bg = '#f0f0f0', height = 471, width = 1129 )
    gridArea.place(relx = 0.03, rely = 0.08)
    variables.setGridArea(gridArea)

    wallButton = tkinter.Button(AStarWindow, bg = '#000000', activebackground = '#303030' , height = 4, width = 9, command = lambda: variables.setCurrentObject('wall')) 
    wallButton.place(relx = 0.03, rely = 0.87)

    startImage = tkinter.PhotoImage(file='startcell.png').zoom(2,2)
    startButton = tkinter.Button(AStarWindow, image= startImage, height = 65, width = 65, bd = 1, command = lambda: variables.setCurrentObject('start')) 
    startButton.place(relx = 0.12, rely = 0.87)
    
    endImage = tkinter.PhotoImage(file='endcell.png').zoom(2,2)
    endButton = tkinter.Button(AStarWindow, image= endImage, height = 65, width = 65, bd = 1, command = lambda: variables.setCurrentObject('end')) 
    endButton.place(relx = 0.21, rely = 0.87)

    puddleImage = tkinter.PhotoImage(file = 'puddle.png').zoom(2,2)
    puddleButton = tkinter.Button(AStarWindow, image= puddleImage, height = 65, width = 65, bd = 1, command = lambda: variables.setCurrentObject('puddle')) 
    puddleButton.place(relx = 0.3, rely = 0.87)

    warpInImage = tkinter.PhotoImage(file = 'warpin.png').zoom(2,2)
    warpInButton = tkinter.Button(AStarWindow, image= warpInImage, height = 65, width = 65, bd = 1, command = lambda: variables.setCurrentObject('warp in')) 
    warpInButton.place(relx = 0.39, rely = 0.87)

    warpOutImage = tkinter.PhotoImage(file = 'warpout.png').zoom(2,2)
    warpOutButton = tkinter.Button(AStarWindow, image= warpOutImage, height = 65, width = 65, bd = 1, command = lambda: variables.setCurrentObject('warp out')) 
    warpOutButton.place(relx = 0.48, rely = 0.87)

    wallLabel = tkinter.Label(AStarWindow, text = 'wall', font = '"OCR A Extended" 17', fg = '#000000', bg = '#ffffff')
    wallLabel.place(relx = 0.035, rely = 0.815)

    startLabel = tkinter.Label(AStarWindow, text = 'start', font = '"OCR A Extended" 17', fg = '#000000', bg = '#ffffff')
    startLabel.place(relx = 0.12, rely = 0.815)

    endLabel = tkinter.Label(AStarWindow, text = 'target', font = '"OCR A Extended" 17', fg = '#000000', bg = '#ffffff')
    endLabel.place(relx = 0.204, rely = 0.815)

    puddleLabel = tkinter.Label(AStarWindow, text = 'puddle', font = '"OCR A Extended" 17', fg = '#000000', bg = '#ffffff')
    puddleLabel.place(relx = 0.295, rely = 0.815)

    warpInLabel = tkinter.Label(AStarWindow, text = 'portal\nin', font = '"OCR A Extended" 17', fg = '#000000', bg = '#ffffff')
    warpInLabel.place(relx = 0.383, rely = 0.785)

    warpOutLabel = tkinter.Label(AStarWindow, text = 'portal\nout', font = '"OCR A Extended" 17', fg = '#000000', bg = '#ffffff')
    warpOutLabel.place(relx = 0.473, rely = 0.785)

    run = tkinter.Button(AStarWindow,  text = 'Run A*', font = '"OCR A Extended" 27', bg = '#ccffe0', activebackground = '#99ffc2', fg = '#000000', relief = 'raised', padx = 15, pady = 20, bd = 6, command = lambda: checkGrid(variables, AStarWindow))
    run.place(relx = 0.586, rely = 0.8)

    clear = tkinter.Button(AStarWindow,  text = 'Clear', font = '"OCR A Extended" 17', bg = '#e2e2e2', activebackground = '#cccccc', fg = '#000000', relief = 'raised', padx = 2, pady = 2, bd = 4, command = lambda: clearGrid(variables))
    clear.place(relx = 0.77, rely = 0.88)

    info = tkinter.Button(AStarWindow,  text = 'What\'s going on?', font = '"OCR A Extended" 17', bg = '#e2e2e2', activebackground = '#cccccc', fg = '#000000', relief = 'raised', padx = 2, pady = 2, bd = 4, command = lambda: infoPage(variables))
    info.place(relx = 0.77, rely = 0.8)

    menu = tkinter.Button(AStarWindow,  text = 'Menu', font = '"OCR A Extended" 17', bg = '#e2e2e2', activebackground = '#cccccc', fg = '#000000', relief = 'raised', padx = 2, pady = 2, bd = 4, command = lambda:returnToMenu(AStarWindow, variables))
    menu.place(relx = 0.91, rely = 0.88)

    #Fill the grid with empty cells
    cellsList = variables.getCellsList()
    allCells = variables.getAllCells()
    images = variables.getImages()
    for x in range(variables.getWidth()):
        for y in range(variables.getHeight()):
            cellsList.append([x, y])
            allCells.append(Cell(x, y, variables.getHeight(), variables.getWidth(), {'background': '#f0f0f0'}))
            images.append('')
        #endfor
    #endfor
    for cell in allCells:
        drawCell(cell, variables)
    #endfor
    variables.setCellsList(cellsList)
    variables.setAllCells(allCells)
    variables.setImages(images)

    #Detect when the user clicks on the grid
    gridArea.bind('<Button-1>', lambda event: addObject(event, variables))
    variables.setGridArea(gridArea)

    AStarWindow.mainloop()
#endsub

#Iniialising A* Simulation

def navigateAStarSimulation():
    variables = AStarClass() #Tkinter buttons do not allow variables to be returned. To avoid this issue I have made each variable an attribute of 'AStarClass', so that they can be accessed, and more importantly, edited by any subroutine where 'variables' is passed in.
    main(variables)
    return variables.getReturnToMenu()
#endsub

