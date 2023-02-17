#The main part of Maze Game

import time
import tkinter
from threading import Thread

try:
    import mysql.connector
except ImportError:
    pass #an error message for this is already produced in the main program
#endtry
    
import randomisedDepthFirstSearch
import spriteClass
import stopwatchClass
import AStarAlgorithm

#Objects

class MazeClass():
    '''This class is used so that variables can be adjusted by functions that are called from a Tkinter button or keypress.'''
    
    def __init__(self, size, username, mazeWindow):
        self.__SIZE = size
        self.__USERNAME = username
        self.__DEFAULT = {'main': '#ffffff', 'text': '#000000', 'accent': '#0000e6', 'background': '#f2f2f2', 'activebutton': '#d9d9d9', 'trail1':'#a6a6a6', 'trail2': '#a6a6a6', 'trail3':'#a6a6a6', 'trail4':'#a6a6a6', 'walls': '#000000'}
        self.__BLUE = {'main': '#e6ffff', 'text': '#000000', 'accent': '#0f008a', 'background': '#80ffff', 'activebutton': '#7ceeee', 'trail1':'#ffffff', 'trail2': '#ffffff', 'trail3':'#ffffff', 'trail4':'#ffffff', 'walls': '#001a66'}
        self.__GREEN = {'main': '#99ffdd', 'text': '#000000', 'accent': '#004d1a', 'background': '#33ff77', 'activebutton': '#00ff55', 'trail1':'#ccffcc', 'trail2': '#ccffcc', 'trail3':'#ccffcc', 'trail4':'#ccffcc', 'walls': '#006600'}
        self.__PINK = {'main': '#ff80d5', 'text': '#000000', 'accent': '#3d004d', 'background': '#ffccf6', 'activebutton': '#ff99ec', 'trail1':'#ff96f1', 'trail2': '#ff96f1', 'trail3':'#ff96f1', 'trail4':'#ff96f1', 'walls': '#ff0000'}
        self.__NEON = {'main': '#000000', 'text': '#ffffff', 'accent': '#ffffcc', 'background': '#4d4d4d', 'activebutton': '#ffff00', 'trail1':'#ff0080', 'trail2': '#1aa3ff', 'trail3':'#8600b3', 'trail4':'#ffff00', 'walls': '#ffffff'}
        self._theme = self.__DEFAULT #the theme currently in use out of the above 5 options
        self._mazeWindow = mazeWindow
        self.__SCALE = 400/size #used for scaling so the maze fills the canvas
        self.__TRANSLATE = self.__SCALE /2 #used to translate cells to the correct position.
        self._mazeArea = tkinter.Canvas(mazeWindow, bd = 0, bg = self._theme['background'], height = 400, width = 400 ) #the tkinter canvas which the maze is drawn on
        self._sprite = spriteClass.Sprite()
        self._spriteImage = None #the image of the sprite that is drawn on the canvas
        self._startImage = None
        self._passages = []
        self._allCells = []
        self._cellsList = []
        self._drawnCells = {} #of the form {cell's xy coordinates : Tkinter rectangle corresponding to this cell}
        self._allWalls = []
        self._drawnWalls = []
        self._finished = False #used to determine whether the congratulations page should be displayed
        self._stopwatch = None
        self._thread = None
        self._topPage = None #a congratulations or themes page which displays while the main page is still open.
        self._changeDifficulty = False
        self._returnToMenu = False   
    #endsub

    def getSize(self):
        return self.__SIZE
    #endsub

    def getUsername(self):
        return self.__USERNAME
    #endsub

    def getDefaultTheme(self):
        return self.__DEFAULT
    #endsub

    def getBlueTheme(self):
        return self.__BLUE
    #endsub

    def getGreenTheme(self):
        return self.__GREEN
    #endsub

    def getPinkTheme(self):
        return self.__PINK
    #endsub

    def getNeonTheme(self):
        return self.__NEON
    #endsub

    def getTheme(self):
        return self._theme
    #endsub

    def setTheme(self, new):
        self._theme = new
    #endsub

    def getMazeWindow(self):
        return self._mazeWindow
    #endsub

    def setMazeWindow(self, new):
        self._mazeWindow = new
    #endsub

    def getScale(self):
        return self.__SCALE
    #endsub

    def getTranslate(self):
        return self.__TRANSLATE
    #endsub

    def getMazeArea(self):
        return self._mazeArea
    #endsub

    def setMazeArea(self, new):
        self._mazeArea = new
    #endsub

    def getSprite(self):
        return self._sprite
    #endsub

    def setSprite(self, new):
        self._sprite = new
    #endsub

    def getSpriteImage(self):
        return self._spriteImage
    #endsub

    def setSpriteImage(self, new):
        self._spriteImage = new
    #endsub

    def getStartImage(self):
        return self._startImage
    #endsub

    def setStartImage(self, new):
        self._startImage = new
    #endsub

    def getPassages(self):
        return self._passages
    #endsub

    def setPassages(self, new):
        self._passages = new
    #endsub

    def getAllCells(self):
        return self._allCells
    #endsub

    def setAllCells(self, new):
        self._allCells = new
    #endsub

    def getCellsList(self):
        return self._cellsList
    #endsub

    def setCellsList(self, new):
        self._cellsList = new
    #endsub

    def getDrawnCells(self):
        return self._drawnCells
    #endsub

    def setDrawnCells(self, new):
        self._drawnCells = new
    #endsub

    def getAllWalls(self):
        return self._allWalls
    #endsub

    def setAllWalls(self, new):
        self._allWalls = new
    #endsub

    def getDrawnWalls(self):
        return self._drawnWalls
    #endsub

    def setDrawnWalls(self, new):
        self._drawnWalls = new
    #endsub

    def getFinished(self):
        return self._finished
    #endsub

    def setFinished(self, new):
        self._finished = new
    #endsub

    def getStopwatch(self):
        return self._stopwatch
    #endsub

    def setStopwatch(self, new):
        self._stopwatch = new
    #endsub

    def getThread(self):
        return self._thread
    #endsub

    def setThread(self, new):
        self._thread = new
    #endsub

    def getTopPage(self):
        return self._topPage
    #endsub

    def setTopPage(self, new):
        self._topPage = new
    #endsub

    def getChangeDifficulty(self):
        return self._changeDifficulty
    #endsub

    def setChangeDifficulty(self, new):
        self._changeDifficulty = new
    #endsub

    def getReturnToMenu(self):
        return self._returnToMenu
    #endsub

    def setReturnToMenu(self, new):
        self._returnToMenu = new
    #endsub
#endclass

class stopwatchThread():
    '''Used to update the stopwatch. Threads run simultaneously with the main program.'''

    def __init__(self, x, variables):
        self._running = True
        self._t = Thread(target = self._updateStopwatch, args = (x, variables))
        self._t.setDaemon(True) #so the thread ends when the window is closed
        self._t.start()
    #endsub

    def stop(self):
        '''Causes the thread to end'''
        self._running = False
    #endsub

    def _updateStopwatch(self, x, variables):
        '''Used to update the displayed stopwatch each time it increments'''
        stopwatch = variables.getStopwatch()
        try:
            minutes = stopwatch.getMinutes()
            while minutes < 60 and variables.getFinished() == False and self._running == True: #don't try to update the stopwatch after one hour or when the maze has been completed
                stopwatch.increment()   
                timeTaken = stopwatch.getDisplay()
                stopwatchDisplay = tkinter.Label(variables.getMazeWindow(), text= timeTaken, font = '"Verdana" 15', fg = variables.getTheme()['accent'], bg = variables.getTheme()['main'])
                stopwatchDisplay.place(relx = 0.45, rely = 0.9)
                time.sleep(1)
                minutes = stopwatch.getMinutes()
            #endwhile 
        except (RuntimeError, tkinter.TclError): #There may be an error if the user closes the program while the thread is running
            pass
        #endtry  
        variables.setStopwatch(stopwatch)
    #endsub
        
    def gett(self):
        return self._t
    #endsub

    def sett(self, new):
        self._t = new
    #endsub
#endclass

#Changing the theme

def closeTopPage(variables):
    '''Properly close the themes or congratulations page'''
    variables.getTopPage().destroy()
    variables.setTopPage(None)
#endsub

def themePage(size, variables):
    '''Produce a page allowing the user to choose a theme'''
    if variables.getTopPage(): #prevent the page from being open more than once at a time
        variables.getTopPage().destroy()
        variables.setTopPage(None)
    #endif
    try:

        themesWindow = tkinter.Tk()
        themesWindow.title('Maze-solving using A*')
        themesWindow.geometry('400x500')
        themesWindow.configure(bg = variables.getTheme()['main'])
        themesWindow.protocol('WM_DELETE_WINDOW', lambda: closeTopPage(variables)) #means if the user closes the window using X this window can be opened again, otherwise the themes button would do nothing.

        title = tkinter.Label(themesWindow, text = 'Select a theme:', font = '"OCR A Extended" 25', fg = variables.getTheme()['text'], bg = variables.getTheme()['main'])
        title.place(relx =0.05, rely = 0.03)

        default = tkinter.Button(themesWindow, text = 'Default', font = '"OCR A Extended" 20', fg = variables.getDefaultTheme()['text'], bg = variables.getDefaultTheme()['background'], activebackground = variables.getDefaultTheme()['activebutton'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:changeTheme(size, variables, themesWindow, variables.getDefaultTheme()))
        default.place(relx = 0.3, rely = 0.15)

        blue = tkinter.Button(themesWindow, text = 'Blue', font = '"OCR A Extended" 20', fg = variables.getBlueTheme()['text'], bg = variables.getBlueTheme()['background'], activebackground=variables.getBlueTheme()['activebutton'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:changeTheme(size, variables, themesWindow, variables.getBlueTheme())) 
        blue.place(relx = 0.35, rely = 0.32)

        green = tkinter.Button(themesWindow, text = 'Green', font = '"OCR A Extended" 20', fg = variables.getGreenTheme()['text'], bg = variables.getGreenTheme()['background'], activebackground=variables.getGreenTheme()['activebutton'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:changeTheme(size, variables, themesWindow, variables.getGreenTheme()))
        green.place(relx = 0.33, rely = 0.49)

        pink = tkinter.Button(themesWindow, text = 'Pink', font = '"OCR A Extended" 20', fg = variables.getPinkTheme()['text'], bg = variables.getPinkTheme()['background'], activebackground=variables.getPinkTheme()['activebutton'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:changeTheme(size, variables, themesWindow, variables.getPinkTheme()))
        pink.place(relx = 0.35, rely = 0.66)

        neon = tkinter.Button(themesWindow, text = 'Neon', font = '"OCR A Extended" 20', fg = variables.getNeonTheme()['text'], bg = variables.getNeonTheme()['background'], activebackground=variables.getNeonTheme()['activebutton'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:changeTheme(size, variables, themesWindow, variables.getNeonTheme()))
        neon.place(relx = 0.35, rely = 0.83)

        variables.setTopPage(themesWindow)

        themesWindow.mainloop()
    except tkinter.TclError: #if the user closes the main maze window this error will occur
        themesWindow.destroy() 
    #endtry
#endsub

def changeTheme(size, variables, themesWindow, newTheme):
    '''Reset the main maze window with the new theme'''
    variables.setTopPage(None)
    themesWindow.destroy()
    variables.setTheme(newTheme)

    #reset the sprite's position
    sprite = variables.getSprite()
    sprite.setxy((0,0))
    variables.setSprite(sprite)

    #end the current stopwatch thread
    thread = variables.getThread()
    thread.stop() 
    t = thread.gett()
    t.join() #ends the thread properly
    thread.sett(t)
    variables.setThread(thread)

    main(size, variables)
#endsub

#Solving the maze

def solveMaze(variables):
    '''Use the A* algorithm to find and display a solution to the maze'''
    
    #find the solution
    solution, a = AStarAlgorithm.AStar(variables.getAllCells()[0], variables.getAllCells()[-1], variables.getAllWalls(), variables.getCellsList(), variables.getAllCells(), None)
    
    #display the solution on the canvas
    for cell in variables.getAllCells()[1:-1]:
        cell.setColour(variables.getTheme()['background']) #clear the grid first
        drawCell(cell, variables)
    #endfor
    for cell in solution[1:-1]: #omit the end cell so congratulations isn't called
        position = variables.getCellsList().index([cell[0], cell[1]])
        cell = variables.getAllCells()[position]
        editCell(cell, variables)
    #endfor
    mazeArea = variables.getMazeArea()
    try:
        for wall in variables.getDrawnWalls():
            mazeArea.tag_raise(wall) #brings the walls to the top layer
        #endfor 
        mazeArea.tag_raise(variables.getSpriteImage())
    except tkinter.TclError: #may be caused when the tkinter window quits
        pass
    #endtry
    variables.setMazeArea(mazeArea)
    variables.setFinished(True) #so no time is recorded
#endsub

#Congratulating the player

def findHighScore(newTime, newTimeDisplay, variables):
    '''Retrieve the user's high score from the database'''
    newHighScore = False

    #find the current difficulty
    size = variables.getSize()
    if size == 5:
        difficulty = 'Easy'
    elif size == 10:
        difficulty = 'Medium'
    elif size == 15:
        difficulty = 'Hard'
    #endif
    
    username = variables.getUsername()
    if username == 'Guest':
        return difficulty, 'XX:XX', newHighScore #for guests the database isn't accessed
    else:
        db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'root', database = 'user_accounts')
        cursor = db.cursor()

        #retrieve the old high score
        if difficulty == 'Easy':
            sql = 'SELECT easy_high_score FROM user_details WHERE username = %s'
        elif difficulty == 'Medium':
            sql = 'SELECT medium_high_score FROM user_details WHERE username = %s'
        elif difficulty == 'Hard':
            sql = 'SELECT hard_high_score FROM user_details WHERE username = %s'
        #endif
        value = (username,)
        cursor.execute(sql, value)
        result = cursor.fetchone()

        if result == (None,): #the user hasn't attempted this difficulty before
            newHighScore = True
            highScore = newTimeDisplay
        else:
            for oldTime in result:
                highScore = oldTime #by default the previous high score is the high score

                #convert to total number of seconds
                minutes = int(oldTime[:2])
                seconds = int(oldTime[3:])
                oldTime = minutes*60 + seconds

                #compare the scores
                if newTime < oldTime:
                    newHighScore = True
                    highScore = newTimeDisplay
                #endif
            #endfor
        #endif

        #update the high score in the database
        if newHighScore:
            if difficulty == 'Easy':
                sql = 'UPDATE user_details SET easy_high_score = %s WHERE username = %s'
            elif difficulty == 'Medium':
                sql = 'UPDATE user_details SET medium_high_score = %s WHERE username = %s'
            elif difficulty == 'Hard':
                sql = 'UPDATE user_details SET hard_high_score = %s WHERE username = %s'
            #endif
            values = (newTimeDisplay, username,)
            cursor.execute(sql, values)
            db.commit()
        #endif

        return difficulty, highScore, newHighScore
    #endif
#endsub

def congratulations(variables):
    '''Produce a page congratulating the user for completing the maze'''

    if variables.getTopPage():
        variables.getTopPage().destroy()
        variables.setTopPage(None)
    #endif

    #check if this score is a new high score
    time = variables.getStopwatch().getTotal()
    timeDisplay = variables.getStopwatch().getDisplay()
    difficulty, highScore, newHighScore = findHighScore(time, timeDisplay, variables)
    
    congratulationsWindow=tkinter.Tk()
    congratulationsWindow.title('Maze-solving using A*')
    congratulationsWindow.geometry('600x450')
    congratulationsWindow.configure(bg = variables.getTheme()['main'])
    congratulationsWindow.protocol('WM_DELETE_WINDOW', lambda: closeTopPage(variables))

    title = tkinter.Label(congratulationsWindow, text = 'CONGRATULATIONS!', font = 'Stencil 40', fg = variables.getTheme()['text'], bg = variables.getTheme()['main'])
    title.place(relx =0.07, rely = 0.03)

    timelabel = tkinter.Label(congratulationsWindow, text = 'Your Time:', font = '"OCR A Extended" 25', fg = variables.getTheme()['text'], bg = variables.getTheme()['main'])
    timelabel.place(relx = 0.35, rely = 0.21)

    score = tkinter.Label(congratulationsWindow, text = timeDisplay, font = '"Verdana" 22 bold', fg = variables.getTheme()['accent'], bg = variables.getTheme()['main'])
    score.place(relx = 0.42, rely = 0.31)

    hslabel = tkinter.Label(congratulationsWindow, text = '{0} High Score:'.format(difficulty), font = '"OCR A Extended" 25', fg = variables.getTheme()['text'], bg = variables.getTheme()['main'])
    hslabel.place(relx = 0.25, rely = 0.47)

    hscore = tkinter.Label(congratulationsWindow, text = highScore, font = '"Verdana" 22 bold', fg = variables.getTheme()['accent'], bg = variables.getTheme()['main'])
    hscore.place(relx = 0.42, rely = 0.57)

    newhs = tkinter.Label(congratulationsWindow, text = '*** NEW HIGH SCORE ***', font = '"OCR A Extended" 20', fg = variables.getTheme()['accent'], bg = variables.getTheme()['main'])
    if newHighScore == True:
        newhs.place(relx = 0.2, rely = 0.72)
    #endif

    back = tkinter.Button(congratulationsWindow, text = 'Back', font = '"OCR A Extended" 15', bg = variables.getTheme()['background'], activebackground=variables.getTheme()['activebutton'], fg = variables.getTheme()['text'], relief = 'raised', padx = 5, pady = 5, bd = 4, command=lambda:closeTopPage(variables))
    back.place(relx = 0.44, rely = 0.84)

    variables.setTopPage(congratulationsWindow)

    congratulationsWindow.mainloop()
#endsub

#Creating the maze

def drawCell(cell, variables):
    '''Draw one of the cells in the maze'''
    xy = cell.getxy() #this is the centre of a cell, so topleft and bottomright are the corners of this cell.
    topleft = (xy[0]-0.5, xy[1]-0.5)
    bottomright = (xy[0]+0.5, xy[1]+0.5)
    global colour
    colour = cell.getColour()
    mazeArea = variables.getMazeArea()
    drawnCells = variables.getDrawnCells()

    #delete the cell if already present. This improves performance after cells have been redrawn lots of times.
    if xy in drawnCells:
        mazeArea.delete(drawnCells[xy])
        del drawnCells[xy]
    #endif


    #draw the cell
    if type(colour) == str:
        rectangle = mazeArea.create_rectangle(topleft[0]*variables.getScale()+variables.getTranslate(), topleft[1]*variables.getScale()+variables.getTranslate(), bottomright[0]*variables.getScale()+variables.getTranslate(), bottomright[1]*variables.getScale()+variables.getTranslate(), fill = colour, outline = colour)
    else: #used by the start and end cell
        #scale the image depending on the maze size
        if variables.getSize() == 5:
            colour = variables.getMazeWindow().colour = colour.zoom(5, 5)
            colour = variables.getMazeWindow().colour = colour.subsample(2, 2)
        elif variables.getSize() == 10:
            colour = variables.getMazeWindow().colour = colour.zoom(5, 5)
            colour = variables.getMazeWindow().colour = colour.subsample(4, 4)
        elif variables.getSize() == 15:
            colour = variables.getMazeWindow().colour = colour.zoom(5, 5)
            colour = variables.getMazeWindow().colour = colour.subsample(6, 6)
        #endif

        if cell.getType() == 'start':
            variables.setStartImage(colour) #This prevents the start cell from being garbage collected and not displaying on the canvas.
            rectangle = mazeArea.create_image(topleft[0]*variables.getScale()+variables.getTranslate(), topleft[1]*variables.getScale()+variables.getTranslate(), image=variables.getStartImage(), anchor='nw')
        else:
            rectangle = mazeArea.create_image(topleft[0]*variables.getScale()+variables.getTranslate(), topleft[1]*variables.getScale()+variables.getTranslate(), image=variables.getMazeWindow().colour, anchor='nw')
        #endif
    #endif
    drawnCells.update({xy:rectangle}) #add this newly drawn cell to drawnCells
    variables.setMazeArea(mazeArea)
    variables.setDrawnCells(drawnCells)
#endsub

def editCell(currentCell, variables):
    '''Check if this is the end cell, and if not, change it's colour.'''
    type=currentCell.getType()
    if type == 'end' and variables.getFinished() == False:
        variables.setFinished(True) #this means the congratulations page is only called once
        congratulations(variables) #call the congratulations page
    elif type == 'empty':
        xy=currentCell.getxy()
        if (xy[0]+ xy[1]) % 4 == 0: #this if statement determines which trail colour to use when using the NEON theme
            currentCell.setColour(variables.getTheme()['trail1'])            
        elif ((xy[0]+ xy[1])) % 4 == 1:
            currentCell.setColour(variables.getTheme()['trail2'])
        elif ((xy[0]+ xy[1])) % 4 == 2:
            currentCell.setColour(variables.getTheme()['trail3'])
        elif ((xy[0]+ xy[1])) % 4 == 3:
            currentCell.setColour(variables.getTheme()['trail4'])
        #endif
        drawCell(currentCell, variables)
    #endif
#endsub

def createWalls(variables):
    '''Use randomised depth-first search to create a list of passages, then generate a corresponding list of walls.'''
    allWalls = []

    #create an instance of each wall, horizontal and vertical. 
    for i in range (0, variables.getSize()):
        for j in range(0, variables.getSize()):
            wall = ((i, j), (i+1, j))
            allWalls.append(wall)
            wall = ((i, j), (i, j+1))
            allWalls.append(wall)
        #endfor
    #endfor
            
    #Translate each wall so that they are drawn around each cell rather than through them. (walls are translated left and up, the right and botton sides of the maze are ignored as those walls wouldn't be seen.)
    newWalls = []
    for wall in allWalls: #eg ((3,2),(4,2)) - this wall will be a horizontal wall above cell (3, 2)
        start = wall[0] #(3,2)
        st1 = start[0] -0.5 #2.5 - between cells (2, y) and (3, y)
        st2 = start[1] -0.5 #1.5
        end = wall[1] #(4,2)
        en1 = end[0] -0.5 #3.5
        en2 = end[1] -0.5 #1.5
        wall = ((st1, st2), (en1, en2)) #((2.5, 1.5), (3.5, 1.5)) This wall is therefore the upper boundary of cell (3,2)
        newWalls.append(wall)
    #endfor
        
    #newWalls is currently a grid. The walls crossed by the list of passages must be removed.
    for p in variables.getPassages():
        for w in newWalls:
            if ((w[0][0]+w[1][0])/2 == (p[0][0]+p[1][0])/2) and ((w[0][1]+w[1][1])/2 == (p[0][1]+p[1][1])/2): #check if the midpoint of the wall and passage match. Midpoint = (startx+endx)/2 or (starty + endy) /2
                newWalls.remove(w)
            #endif
        #endfor
    #endfor
    variables.setAllWalls(newWalls)
#endsub

def drawWalls(variables):
    '''Given the list of walls, draw them on the maze'''
    drawnWalls = []
    mazeArea = variables.getMazeArea()
    
    for wall in variables.getAllWalls():
        start = wall[0]
        end = wall[1]
        drawnWalls.append(mazeArea.create_line((start[0])*variables.getScale()+variables.getTranslate()+1, (start[1])*variables.getScale()+variables.getTranslate()+1, (end[0])*variables.getScale()+variables.getTranslate()+1, (end[1])*variables.getScale()+variables.getTranslate()+1, fill=variables.getTheme()['walls'], width = 2))
    #endfor
    variables.setDrawnWalls(drawnWalls)
    variables.setMazeArea(mazeArea)
#endsub

def drawSprite(variables, size):
    '''Draw the sprite onto the maze'''
    xy = variables.getSprite().getxy()
    s = variables.getMazeWindow().s = tkinter.PhotoImage(file='sprite.png')
    #scale the sprite depending on the size of the maze 
    if size == 5:
        s = variables.getMazeWindow().s = s.zoom(2, 2)
    elif size == 15:
        s = variables.getMazeWindow().s = s.zoom(3, 3) #the values in zoom and subsample must be integers. This is the equivalent of *3 then /4, = *0.75.
        s = variables.getMazeWindow().s = s.subsample(4, 4)
    #endif   
    mazeArea = variables.getMazeArea()
    spriteImage = mazeArea.create_image(xy[0]+variables.getTranslate() - int(0.75*(variables.getTranslate()))-1, xy[1]+variables.getTranslate() - int(0.75*(variables.getTranslate()))-1, image=s, anchor='nw')
    try:
        mazeArea.tag_raise(spriteImage)
    except tkinter.TclError: #may be caused when the tkinter window quits
        pass
    #endtry
    variables.setSpriteImage(spriteImage)
    variables.setMazeArea(mazeArea)
#endsub
        
def createMaze(variables):
    '''Call the relevant subroutines to create and display the maze'''
    
    #create a new maze
    passages, allCells, cellsList = randomisedDepthFirstSearch.main(variables.getSize(), variables.getTheme())
    variables.setAllCells(allCells)
    variables.setCellsList(cellsList)
    variables.setPassages(passages)

    #draw the cells
    for cell in variables.getAllCells():
        drawCell(cell, variables)
    #endfor

    #draw the walls
    createWalls(variables)
    drawWalls(variables)

    #position the sprite
    sprite = variables.getSprite()
    oldxy = sprite.getxy()
    mazeArea = variables.getMazeArea()
    mazeArea.move(variables.getSpriteImage(), (oldxy[0]*-1*variables.getScale()), (oldxy[1]*-1*variables.getScale())) #the -1 moves it back to (0, 0)
    try:
        mazeArea.tag_raise(variables.getSpriteImage())
    except tkinter.TclError: #may be caused when the tkinter window quits
        pass
    #endtry
    variables.setMazeArea(mazeArea)
    sprite.setxy((0,0)) #reset the sprite's coordinates
    variables.setSprite(sprite)

    variables.setFinished(False)

    #reset the stopwatch
    stopwatch = variables.getStopwatch()
    stopwatch.reset()
    variables.setStopwatch(stopwatch)
    thread = variables.getThread()
    if thread:        
        thread.stop() #close the current thread before opening a new one
    #endif
    variables.setThread(stopwatchThread([], variables)) #allows the stopwatch to run in the background
#endsub

#Playing the maze

def moveSprite(direction, variables):
    '''Move the sprite in the given direction if there is a passage there'''
    #check if there is a passage in this direction
    move, movement = variables.getSprite().canMove(direction, variables.getCellsList(), variables.getAllCells())

    if move:
        mazeArea = variables.getMazeArea()
        mazeArea.move(variables.getSpriteImage(), movement[0]*variables.getScale(), movement[1]*variables.getScale()) #moves the image one cell in the given direction
        variables.setMazeArea(mazeArea)
        currentCell = variables.getSprite().getCell(variables.getCellsList(), variables.getAllCells())
        editCell(currentCell, variables)
        try:        
            for wall in variables.getDrawnWalls():
                mazeArea.tag_raise(wall) #brings the walls to the top layer (visible above the newly drawn cell)
            #endfor 
            mazeArea.tag_raise(variables.getSpriteImage())
        except tkinter.TclError: #may be caused when the tkinter window quits
            pass
        #endtry
        variables.setMazeArea(mazeArea)
    #endif
#endsub

#Exiting Maze Game      
       
def changeDifficulty(variables):
    '''Exit Maze Section and return to the difficulty selection screen'''
    thread = variables.getThread()
    thread.stop() #terminate the thread before closing the window
    t = thread.gett()
    t.join()
    variables.getMazeWindow().destroy()
    if variables.getTopPage():
        variables.getTopPage().destroy()
    #endif
    variables.setChangeDifficulty(True)
#endsub

def returnToMenu(variables):
    '''Exit Maze Section and return to the menu'''
    thread = variables.getThread()
    thread.stop() #terminate the thread before closing the window
    t = thread.gett()
    t.join()
    variables.getMazeWindow().destroy()
    if variables.getTopPage():
        variables.getTopPage().destroy()
    #endif
    variables.setReturnToMenu(True)
#endsub

#Main window
def closeWindows(mazeWindow, variables):
    '''Close the congratulations or themes window if the user closes the main window'''
    mazeWindow.destroy()
    if variables.getTopPage():
        variables.getTopPage().destroy()
    #endif
#endsub
        
def main(size, variables):
    '''The main subroutine for Maze Game, used to handle tkinter output and call subroutines to set up and play the maze'''

    #Produce the background window
    mazeWindow = variables.getMazeWindow()

    mazeWindow.title('Maze-solving using A*')
    mazeWindow.geometry('800x500')

    mazeWindow.configure(bg= variables.getTheme()['main'])

    mazeWindow.protocol('WM_DELETE_WINDOW', lambda: closeWindows(mazeWindow, variables))

    mazeArea = variables.getMazeArea()
    mazeArea.pack(anchor = 'nw', padx = 30, pady = 30) 
    variables.setMazeArea(mazeArea)

    instructions = tkinter.Label(mazeWindow, text = 'Use the arrow keys\nto move.', justify= 'left', fg= variables.getTheme()['text'], bg= variables.getTheme()['main'], font = '"OCR A Extended" 20')
    instructions.place(relx = 0.59, rely = 0.06)

    variables.setStopwatch(stopwatchClass.Stopwatch()) 
    
    newButton = tkinter.Button(mazeWindow, text = 'New Maze', font = '"OCR A Extended" 15', bg = variables.getTheme()['background'], activebackground=variables.getTheme()['activebutton'], fg = variables.getTheme()['text'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda: createMaze(variables))
    newButton.place(relx = 0.59, rely = 0.25)

    difficultyButton = tkinter.Button(mazeWindow, text = 'Difficulty', font = '"OCR A Extended" 15', bg = variables.getTheme()['background'], activebackground=variables.getTheme()['activebutton'], fg = variables.getTheme()['text'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:changeDifficulty(variables))
    difficultyButton.place(relx = 0.59, rely = 0.38)

    answerButton = tkinter.Button(mazeWindow, text = 'Solution', font = '"OCR A Extended" 15', bg = variables.getTheme()['background'], activebackground=variables.getTheme()['activebutton'], fg = variables.getTheme()['text'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:solveMaze(variables))
    answerButton.place(relx = 0.59, rely = 0.51)

    themeButton = tkinter.Button(mazeWindow, text = 'Theme', font = '"OCR A Extended" 15', bg = variables.getTheme()['background'], activebackground=variables.getTheme()['activebutton'], fg = variables.getTheme()['text'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:themePage(size, variables))
    themeButton.place(relx = 0.59, rely = 0.64)

    menuButton = tkinter.Button(mazeWindow, text = 'Menu', font = '"OCR A Extended" 15', bg = variables.getTheme()['background'], activebackground=variables.getTheme()['activebutton'], fg = variables.getTheme()['text'], relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda: returnToMenu(variables))
    menuButton.place(relx = 0.85, rely = 0.85)

    #Draw the sprite for the first time
    drawSprite(variables, size)
    mazeArea = variables.getMazeArea()
    try:
        mazeArea.tag_raise(variables.getSpriteImage())
    except tkinter.TclError: #may be caused when the tkinter window quits
        pass
    #endtry
    variables.setMazeArea(mazeArea)

    #Create the maze 
    createMaze(variables)

    #Bind keyboard inputs to moving the sprite
    mazeWindow.bind('<Left>', lambda event: moveSprite('left', variables))
    mazeWindow.bind('<Right>', lambda event: moveSprite('right', variables))
    mazeWindow.bind('<Up>', lambda event: moveSprite('up', variables))
    mazeWindow.bind('<Down>', lambda event: moveSprite('down', variables))

    variables.setMazeWindow(mazeWindow)
    variables.getMazeWindow().mainloop()
#endsub

#Initialising Maze Game

def navigateMazeSection(size, username):
    '''Call main using the default theme, and exit if changeDifficulty or returnToMenu become true.'''

    mazeWindow = tkinter.Tk()
    variables = MazeClass(size, username, mazeWindow) #Tkinter buttons do not allow variables to be returned. To avoid this issue I have made each variable an attribute of 'MazeClass', so that they can be accessed, and more importantly, edited by any subroutine where 'variables' is passed in. 
    
    main(size, variables)
    return variables.getChangeDifficulty(), variables.getReturnToMenu()
#endsub

