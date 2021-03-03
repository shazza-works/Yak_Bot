#!/usr/bin/python3
#
# Azzassin 30/10/2020
# Shazza-Works
#
import sqlite3

class tc:
    head = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    nc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

conn = sqlite3.connect("score.db")
c = conn.cursor()

def addUser(userID):
    response = checkUserScore(userID)
    if response != None : #User account already exists
        return (False ,response[0])
    c.execute("INSERT INTO scoreboard (userid, score, datestarted) VALUES (?, 0, datetime('now'))", (userID,))
    conn.commit()
    return (True, 0)

def checkUserScore(userID):
    c.execute("SELECT score FROM scoreboard WHERE userid=?", (userID,))
    return c.fetchone()

def callScoreBoard():
    c.execute("SELECT userid, score FROM scoreboard order by score desc")
    return c.fetchall()

def getAccDate(userID):
    c.execute("SELECT datestarted FROM scoreboard WHERE userid=?", (userID,))
    return c.fetchone()

def addPoints(userID, pointsToAdd):
    points = checkUserScore(userID)
    if points == None : #No user account
        return 0
    totalPoints = points[0] + int(pointsToAdd)
    c.execute("UPDATE scoreboard set score = ? where userid=?", (totalPoints, userID,))
    conn.commit()
    return totalPoints

def checkHash(clearText, crack):
    statements = (clearText, crack)
    c.execute("SELECT points FROM hashes where cleartext=? and hash=? and cracked=0", statements)
    response = c.fetchone()
    if response == None :
        return 0
    points = response[0]
    c.execute("UPDATE hashes set cracked=1 where cleartext=? and hash=?",statements)
    conn.commit()
    return points

def addHash(clearText, crack, points):
    statements = (clearText, crack, points)
    c.execute("INSERT INTO hashes (clearText, hash, points, cracked) VALUES (?, ?, ?, 0)", statements)
    conn.commit()

def getPool():
    c.execute("SELECT points, hash FROM hashes where cracked=0")
    response = c.fetchall()
    return response

def getUserWelcome():
    c.execute("SELECT userid FROM users")
    response = c.fetchall()
    return response

def addUserWelcome(userID):
    c.execute("INSERT INTO users (userid) VALUES (?)", (userID,))
    conn.commit()

def purgeUser(userID):
    c.execute("DELETE FROM users WHERE userid=(?)", (userID,))
    conn.commit()
    print (tc.red, "[!] Removed ID={} from Users Welcome DB.".format(userID), tc.nc)

def purgeScore(userID):
    c.execute("DELETE FROM scoreboard WHERE userid=(?)", (userID,))
    conn.commit()
    print (tc.red, "[!] Removed ID={} from Scores DB.".format(userID), tc.nc)

def wipePool():
    c.execute("DELETE FROM hashes where cracked=0")
    conn.commit()
    print (tc.red, "[!] Wipe of HASH pool done in Scores DB.", tc.nc)
