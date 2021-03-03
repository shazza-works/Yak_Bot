#!/usr/bin/python3.8
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

def wipe_db():
	conn = sqlite3.connect("score.db")
	c = conn.cursor()
	print (tc.green, "[*] Connected to database scores.db", tc.nc)

	c.execute("DROP TABLE IF EXISTS users")
	print (tc.red, "[*] Dropped Table; users", tc.nc)

	c.execute("DROP TABLE IF EXISTS easy_passwords")
	print (tc.red, "[*] Dropped Table; easy_passwords", tc.nc)

	c.execute("DROP TABLE IF EXISTS scoreboard")
	print (tc.red, "[*] Dropped Table; scoreboard", tc.nc)

	c.execute("DROP TABLE IF EXISTS hashes")
	print (tc.red, "[*] Dropped Table; hashes", tc.nc)

	c.execute('''CREATE TABLE users (
		userid integer);''')
	print (tc.green, "[*] Created Table; users", tc.nc)

	c.execute('''CREATE TABLE scoreboard (
		id integer primary key,
		userid text,
		score int,
		datestarted text);''')
	print (tc.green, "[*] Created Table; scoreboard", tc.nc)

	c.execute('''CREATE TABLE hashes (
		id integer primary key,
		cleartext text,
		hash text,
		points int,
		cracked int);''')
	print (tc.green, "[*] Created Table; hashes", tc.nc)

	c.execute('''CREATE TABLE easy_passwords (
		id integer primary key,
		password text,
		hash text);''')
	print (tc.green, "[*] Created Table; easy_passwords", tc.nc)

	print (tc.blue, "[!] DB has beeen Wiped!", tc.nc)
	conn.commit()
