import hashlib #to hash passwords

def register(username, password, db):
    '''Allow users to create a new account'''

    #check if the chosen username is already in use
    if username == 'Guest':
        return False #as this is the guest account
    #endif
    cursor = db.cursor()
    cursor.execute('SELECT username FROM user_details')
    for names in cursor:
        for name in names:
            if name == username:
                return False #so the program doesn't continue
            #endif
        #endif
    #endfor

    #hash the user's password using SHA256 so it is unrecognisable
    password = str(hashlib.sha256(password.encode('utf-8')).hexdigest())

    #add a record to the database with None in the high score fields
    sql = 'INSERT INTO user_details (username, password) VALUES (%s, %s)'
    values = (username, password)
    cursor.execute(sql, values)
    db.commit()

    return True
#endsub

def signIn(username, password, db):
    '''Allow the user to sign in to their existing account'''

    #lookup the password hash in the database
    cursor = db.cursor()
    sql = 'SELECT password FROM user_details WHERE username = %s'
    value = (username, )
    cursor.execute(sql, value)

    result = cursor.fetchone()
    if result:
        for oldhash in result:
            
            #calculate the hash of the newly typed password and check against this hash
            newhash = str(hashlib.sha256(password.encode('utf-8')).hexdigest())
            if oldhash == newhash:
                return True
            #endif
        #endfor

    else:
        return False #the username was not in the database
    #endif
#endsub
