import sqlite3
from datetime import datetime
import re
import hashlib


# returns True if the new password hash matches the one stored in the .db file, as well as the username
# otherwise, it returns an error message
def login(u_in, pass_in):
    pass_hash = hash_password(pass_in)
    conn = sqlite3.connect('Checkers_Game.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute("SELECT * FROM Users WHERE Username = ? and Password = ?", (u_in, pass_hash,))

    if c.fetchall():
        return True
    else:
        return 'Incorrect Username or Password'

# enters a username, hashed password, and unique user ID to database if the username and password are valid
# otherwise, it returns an error message
def signup(username, pass_1, pass_2):

    conn = sqlite3.connect("Checkers_Game.db")
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    is_valid = input_check(c, username, pass_1, pass_2)
    
    if is_valid != True:
        return is_valid
    
    password_hash = hash_password(pass_1)

    c.execute("INSERT INTO Users (UserID, Username, Password) VALUES (NULL, ?, ?)", (username, password_hash,))
    conn.commit()
    conn.close()
    return True

# updates username, given that the new username is valid and the password is correct
def update_username(old_user, new_user, password):
    conn = sqlite3.connect('Checkers_Game.db')
    c = conn.cursor()
    is_valid = input_check(c, new_user)

    if is_valid != True:
        return is_valid
    
    pass_hash = hash_password(password)
    
    c.execute("UPDATE Users SET Username = ? WHERE Username = ? AND Password = ?", (new_user, old_user, pass_hash))
    conn.commit()
    conn.close()
    return True

# updates password if username and old password are in the .db file and the new password is valid
def update_password(username, old_pass, n_pass_1, n_pass_2):
    conn = sqlite3.connect('Checkers_Game.db')
    c = conn.cursor()
    is_valid = input_check(c, pass_1=n_pass_1, pass_2=n_pass_2)

    if is_valid != True:
        return is_valid
    
    pass_hash = hash_password(old_pass)
    new_pass_hash = hash_password(n_pass_1)
    c.execute("UPDATE Users SET Password = ? WHERE Username = ? AND Password = ?", (new_pass_hash, username, pass_hash))
    conn.commit()
    conn.close()
    return True

# removes all data related to the deleted account from the database
# this includes their game history
def account_deleter(username, password):
    conn = sqlite3.connect('Checkers_Game.db')
    c = conn.cursor()

    hashed_password = hash_password(password)

    c.execute("SELECT UserID from Users WHERE Username = ? AND Password = ?", (username, hashed_password))
    uID = c.fetchone()[0]
    c.execute("""   SELECT Games.GameID
                    FROM Users
                    INNER JOIN GameParticipants ON Users.UserID = GameParticipants.UserID
                    INNER JOIN Games ON GameParticipants.GameID = Games.GameID
                    WHERE Users.UserID = ?
                    """, (uID,))
    gID = c.fetchall()
    for ID in gID:
        c.execute("DELETE FROM Games WHERE GameID = ?", (ID[0],))
    c.execute("DELETE FROM Users WHERE UserID = ?", (uID,))
    c.execute("DELETE FROM GameParticipants WHERE UserID = ?", (uID,))

    conn.commit()
    conn.close()

# checks validity of incoming usernames and passwords using regular expressions
def input_check(c, username=None, pass_1=None, pass_2=None):
    if username != None:
        # at least 1 uppercase and 1 lowercase character
        allowed_user_string = r"^(?=.*[A-Z])(?=.*[a-z])[a-zA-Z0-9._-]+$"

        c.execute("SELECT Username FROM Users WHERE Username = ?", (username,))

        if c.fetchall():
            return 'Username taken'
        if len(username) < 6 or len(username) > 15 or re.search("\s", username) or not re.match(allowed_user_string, username):
            return 'Invalid username'
    
    if pass_1 != None and pass_2 != None:
        # at least 1 uppercase character, 1 lowercase character, 1 numbers and a special character from the given selection
        allowed_pass_string = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[._!@()/:-])[a-zA-Z0-9._!@()/:-]+$"
        if pass_1 != pass_2 or  len(pass_1) < 8 or len(pass_1) > 12 or not re.match(allowed_pass_string, pass_1):
            return 'Invalid password'
    return True

# uses hashlib to run a hashing algorithm on a given password and returns the hex value for it
def hash_password(password):
    hash = hashlib.sha256()
    hash.update(password.encode())
    return hash.hexdigest()

# enters game information to games table
def Games_entry(is_ai):
    conn = sqlite3.connect('Checkers_Game.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    if is_ai: ai_in_db = 1
    else: ai_in_db = 0
    cur_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    c.execute("INSERT INTO Games (GameID, AI, GameDate) VALUES (NULL, ?, ?)", (ai_in_db, cur_time,))
    conn.commit()
    c.execute("SELECT GameID FROM Games WHERE GameDate = ?", (cur_time,))
    game_id = c.fetchone()

    conn.close()
    return game_id

# inputs data linking the user playing the game to the game played in a table in the database
def GameParticipants_entry(username, game_id, IsWinner):
    conn = sqlite3.connect('Checkers_Game.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
    u_id = c.fetchone()
    c.execute("INSERT INTO GameParticipants (GameID, UserID, IsWinner) VALUES (?, ?, ?)", (game_id[0], u_id[0], IsWinner))

    conn.commit()
    conn.close()

# searches gameParticipants table to find all isWinner values for each game
# tallies up each win, draw, and loss that the player has had and returns them
# Uses INNER JOIN to simplify queries and reduce processing
def find_wins(username):
    conn = sqlite3.connect('Checkers_Game.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute("""   SELECT GameParticipants.IsWinner
                    FROM Users
                    INNER JOIN GameParticipants ON Users.UserID = GameParticipants.UserID
                    WHERE Users.Username = ?
              """, (username,))

    wins = losses = draws = 0
    for entry in c.fetchall():
        if entry[0] == 1:
            wins += 1
        elif entry[0] == 0:
            losses += 1
        else:
            draws += 1

    return wins, draws, losses






# makes Users table
def make_table_Users():
    conn = sqlite3.connect("Checkers_Game.db")
    conn.execute("PRAGMA foreign_keys = ON")

    
    c = conn.cursor()
    c.execute("""CREATE TABLE Users (
            UserID integer PRIMARY KEY AUTOINCREMENT,
            Username text NOT NULL,
            Password text NOT NULL
            )""")

    conn.commit()
    conn.close

# makes Games table
def make_table_Games():
    conn = sqlite3.connect('Checkers_Game.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute("""CREATE TABLE Games (
            GameID integer PRIMARY KEY AUTOINCREMENT,
            AI integer NOT NULL,
            GameDate text NOT NULL
            )""")
    

    conn.commit()
    conn.close

# makes GameParticipants table
def make_table_GameParticipants():
    conn = sqlite3.connect('Checkers_Game.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute("""CREATE TABLE GameParticipants (
                GameID integer NOT NULL,
                UserID integer NOT NULL,
                IsWinner integer NOT NULL,
                PRIMARY KEY (UserID, GameID),
                FOREIGN KEY (GameID) REFERENCES Games(GameID),
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )""")
    
    conn.commit()
    conn.close()

# Outputs contents of Users entity for testing
def QueryUsers(username):
    conn = sqlite3.connect('Checkers_Game.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    c.execute("SELECT * FROM USERS WHERE Username = ?", (username,))
    print(c.fetchall())
