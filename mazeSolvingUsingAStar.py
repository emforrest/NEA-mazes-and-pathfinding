#Maze-solving using A*
#Computer Science Non-Examined Assessment 2021 - 2022
#Eleanor Forrest   Candidate Number: 6084   Centre Number: 57017

#Python Code

#Imports
import tkinter
from tkinter import messagebox

try:
    import mysql.connector
    databaseError = False
except ImportError:
    databaseError = True #once the first window is created the user can be warned that there was an error. Else an error message would be produced with a blank window.
#endtry
    
import userAccountManagement
import mazeGame
import AStarSimulation

#User Account Management

def displayLogin():
    '''Produce the display allowing the user to choose whether to register or sign in to an account.'''

    loginWindow = tkinter.Tk()
    loginWindow.title('Maze-solving using A*')
    loginWindow.geometry('600x400')
    loginWindow.configure(bg='#ffffff')

    title = tkinter.Label(loginWindow, text = 'Maze-solving using A*', bg= '#ffffff', font = '"Stencil" 35  underline', )
    title.place(relx= 0.06, rely= 0.13)

    registerButton = tkinter.Button(loginWindow, bg='#ff7070', activebackground='#dd5050', bd='5',  text= 'Register', font= '"OCR A Extended" 25', fg='#000000', padx='10', pady='20', justify='center', relief='raised', command=lambda: navigate('register', loginWindow, None))
    registerButton.place(relx = 0.07, rely = 0.4)

    signInButton = tkinter.Button(loginWindow, bg='#80ffb0', activebackground='#60dd90', bd= '5', text= 'Sign in', font= '"OCR A Extended" 25', fg='#000000', padx='20', pady= '20', justify='center', relief='raised', command=lambda: navigate('sign in', loginWindow, None))
    signInButton.place(relx = 0.57, rely = 0.4)

    guestButton = tkinter.Button(loginWindow, bg='#c5ffff', activebackground = '#a9f0f9',  bd= '5', text= 'Play as guest', font= '"OCR A Extended" 15', fg='#000000', padx='10', pady= '10', justify='center', relief='raised', command=lambda: navigate('menu', loginWindow, 'Guest'))
    guestButton.place(relx = 0.33, rely = 0.75)

    if databaseError:
        messagebox.showwarning(title = 'Maze solving using A*', message = 'There was an issue connecting to the database. You can still play as guest.')
        registerButton['state'] = 'disabled'
        signInButton['state'] = 'disabled'
    #endif
    
    loginWindow.mainloop()
#endsub

def displayForm(option):
    '''Produce the form into which the user can input a username or password.'''

    formWindow=tkinter.Tk()
    formWindow.title('Maze-solving using A*')
    formWindow.geometry('600x400')
    formWindow.configure(bg= '#ffffff')

    usernameLabel = tkinter.Label(formWindow, text='Username:', font= '"OCR A Extended" 25', fg='#000000', bg = '#ffffff'  )
    usernameLabel.place(relx= '0.1', rely= '0.12')

    usernameForm = tkinter.Entry(formWindow, bg = '#f0f0f0', fg = '#000000', width = '15', font = '"Verdana" 14', bd='3')
    usernameForm.place(relx = '0.1', rely ='0.25' )

    passwordLabel = tkinter.Label(formWindow, text='Password:', font= '"OCR A Extended" 25', fg='#000000', bg = '#ffffff'  )
    passwordLabel.place(relx= '0.1', rely= '0.42')

    passwordForm = tkinter.Entry(formWindow, bg = '#f0f0f0', fg = '#000000', width = '15', font = '"Verdana" 14', bd='3', show='*' )
    passwordForm.place(relx = '0.1', rely ='0.55' )

    if option == 'register':
        submitButton = tkinter.Button(formWindow, bg='#ccffe0', activebackground='#aaddc0', bd= 3, fg= '#000000', font='"OCR A Extended" 20', text='Submit', command=lambda: register(usernameForm.get(), passwordForm.get(), formWindow))
    elif option == 'sign in':
        submitButton = tkinter.Button(formWindow, bg='#ccffe0', activebackground='#aaddc0', bd= 3, fg= '#000000', font='"OCR A Extended" 20', text='Submit', command=lambda: signIn(usernameForm.get(), passwordForm.get(), formWindow))
    #endif
    submitButton.place(relx='0.1', rely = '0.75')

    backButton = tkinter.Button(formWindow, text = 'Back', font = '"OCR A Extended" 20', bg = '#e2e2e2', activebackground='#cccccc', fg = '#000000', relief = 'raised', padx = 0, pady = 0, bd = 4, command=lambda: navigate('display login', formWindow, None))
    backButton.place(relx = 0.77, rely = 0.75)

    formWindow.mainloop()
#endsub

def register(username, password, window):
    '''Allow the user to register a new account'''
    #prevent null inputs
    if username.isspace() or username == '':
        messagebox.showwarning(title = 'Maze solving using A*', message = 'Please enter a username.')
    elif password.isspace() or password == '':
        messagebox.showwarning(title = 'Maze solving using A*', message = 'Please enter a password.')
    elif len(username) >256:
        messagebox.showwarning(title = 'Maze solving using A*', message = 'The username is too long.')
    elif len(password) >256:
        messagebox.showwarning(title = 'Maze solving using A*', message = 'The password is too long.')
    else:

        try:
            db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'root', database = 'user_accounts') #attempt to connect to the database
            success = userAccountManagement.register(username, password, db)
            if success:
                messagebox.showinfo(title = 'Maze solving using A*', message = 'Successfully registered {0}.'.format(username))
                navigate('menu', window, username)
            else:
                messagebox.showwarning(title = 'Maze solving using A*', message = 'That username is already in use. Please pick another.')
            #endif
        except mysql.connector.errors.ProgrammingError: #the current device successfully imported mysql.connector but could not connect to this specific database.
            messagebox.showwarning(title = 'Maze solving using A*', message = 'There was an issue connecting to the database. You can still play as a guest.')
            navigate('menu', window, 'Guest')
        #endtry 
    #endif       
#endsub    

def signIn(username, password, window):
    '''Allow a user to sign in to an existing account'''
    #prevent null inputs
    if username.isspace() or username == '':
        messagebox.showwarning(title = 'Maze solving using A*', message = 'Please enter a username.')
    elif password.isspace() or password == '':
        messagebox.showwarning(title = 'Maze solving using A*', message = 'Please enter a password.')
    else:

        try:
            db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'root', database = 'user_accounts') #attempt to connect to the database
            success = userAccountManagement.signIn(username, password, db)
            if success:
                messagebox.showinfo(title = 'Maze solving using A*', message = 'Welcome {0}.'.format(username))
                navigate('menu', window, username)
            else:
                messagebox.showwarning(title = 'Maze solving using A*', message = 'The username or password is incorrect.')
            #endif
        except mysql.connector.errors.ProgrammingError:
            messagebox.showwarning(title = 'Maze solving using A*', message = 'There was an issue connecting to the database. You can still play as a guest.')
            navigate('menu', window, 'Guest')
        #endtry   
    #endif     
#endsub

#Menu

def displayMenu(username):
    '''Produce the menu for the user to choose which game mode to play'''

    menuWindow=tkinter.Tk()
    menuWindow.title('Maze-solving using A*')
    menuWindow.geometry('600x400')
    menuWindow.configure(bg= '#ffffff')

    userLabel= tkinter.Label(menuWindow, text='User: {0}'.format(username), font= '"OCR A Extended" 25', fg='#000000', bg = '#ffffff')
    userLabel.place(relx = 0.25, rely = 0.1)

    mazeButton = tkinter.Button(menuWindow, bg='#3de3d2', activebackground = '#1dc9b8', bd='5',  text= 'Maze Game', font= '"OCR A Extended" 20 bold', fg='#000000', padx='10', pady='40', justify='center', relief='raised', command=lambda: navigate('maze', menuWindow, username))
    mazeButton.place(rely='0.35', relx='0.07')

    aStarButton = tkinter.Button(menuWindow, bg='#639aff', activebackground = '#337aff', bd= '5', text= 'A*\nSimulation', font= '"OCR A Extended" 20 bold', fg='#000000', padx='10', pady= '25', justify='center', relief='raised', command=lambda: navigate('A*', menuWindow, username))
    aStarButton.place(rely='0.35', relx= '0.57' )

    signOutButton = tkinter.Button (menuWindow, bg='#e2e2e2', activebackground='#cccccc',bd= '4', text= 'Sign out', font= '"OCR A Extended" 15', fg='#000000', padx='10', pady= '10', justify='center', relief='raised', command=lambda: navigate('display login', menuWindow, None))
    signOutButton.place(rely='0.77', relx= '0.71' )

    menuWindow.mainloop()
#endsub

#Maze Game

def mazeDifficulty(username):
    '''Allow the user to select a difficulty for the maze'''
    
    mazeDifficultyWindow=tkinter.Tk()
    mazeDifficultyWindow.title('Maze-solving using A*')
    mazeDifficultyWindow.geometry('600x400')
    mazeDifficultyWindow.configure(bg= '#ffffff')

    var = tkinter.IntVar() #contains the size the maze should be based on which difficulty is picked.

    text = tkinter.Label(mazeDifficultyWindow,  text = 'Select a difficulty:', bg= '#ffffff', font = '"OCR A Extended" 25 ', fg = '#000000' )
    text.place(relx= '0.1', rely= '0.07')

    easy = tkinter.Radiobutton(mazeDifficultyWindow, text = 'Easy', font = '"OCR A Extended" 20', bg = '#80ffb0', activebackground='#4dff91', fg = '#000000', bd = 3, relief= 'raised', variable = var, value = 5)
    easy.place(relx = '0.15', rely = 0.25)

    medium = tkinter.Radiobutton(mazeDifficultyWindow, text = 'Medium', font = '"OCR A Extended" 20', bg = '#ffffb3', activebackground='#ffff80', fg = '#000000', bd = 3, relief= 'raised', variable = var, value = 10)
    medium.place(relx = '0.15', rely = 0.45)

    hard = tkinter.Radiobutton(mazeDifficultyWindow, text = 'Hard', font = '"OCR A Extended" 20', bg = '#ff7070', activebackground='#ff4d4d', fg = '#000000', bd = 3, relief= 'raised', variable = var, value = 15)
    hard.place(relx = '0.15', rely = 0.65)

    selectButton = tkinter.Button(mazeDifficultyWindow, text = 'Select', font = '"OCR A Extended" 23', bg = '#c5ffff', activebackground = '#a9f0f9', fg = '#000000', relief = 'raised', padx = 10, pady = 15, bd = 4, command=lambda:getSize(mazeDifficultyWindow, var, username))
    selectButton.place(relx = 0.57, rely = 0.4)

    backButton = tkinter.Button(mazeDifficultyWindow, text = 'Back', font = '"OCR A Extended" 15', bg = '#e2e2e2', activebackground = '#cccccc', fg = '#000000', relief = 'raised', padx = 5, pady = 5, bd = 4, command = lambda:navigate('menu', mazeDifficultyWindow, username))
    backButton.place(relx = 0.82, rely = 0.8)

    mazeDifficultyWindow.mainloop()
#endsub

def getSize(window, var, username):
    '''Retrieve the size of the maze and call Maze Game'''
    
    size = var.get()
    if size == 0: #no button was selected
        messagebox.showwarning(title = 'Maze solving using A*', message = 'Please select a difficulty.')
    else:
        window.destroy()
        changeDifficulty, returnToMenu = mazeGame.navigateMazeSection(size, username) # call Maze Game

        #redirect to the correct page
        if changeDifficulty == True:
            navigate('maze', None, username) 
        elif returnToMenu == True:
            navigate('menu', None, username)
        #endif
    #endif
#endsub

#Navigation

def navigate(option, window, username):
    '''Navigate between different parts of the program.'''
    
    if window:
        window.destroy() #closes the current window
    #endif

    if option == 'display login':
        displayLogin()
    elif option == 'register' or option == 'sign in':
        displayForm(option)
    elif option == 'menu':
        displayMenu(username)
    elif option == 'maze':        
        mazeDifficulty(username)
    elif option == 'A*':
        AStarSimulation.navigateAStarSimulation() #call A* Simulation
        navigate('menu', None, username)
    #endif
#endsub

if __name__ == '__main__':
    navigate('display login', None, None)
#endif
