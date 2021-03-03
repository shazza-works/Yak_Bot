#!/usr/bin/python3.8
#
#
import sys, os
import sqlite3


conn = sqlite3.connect("score.db")
c = conn.cursor()

try:
    word_list = sys.argv[1]
except IndexError:
    print ("Please give me a wordlist first> ", sys.argv[0], "some_wordlist_file.lst")
    sys.exit(1)
except FileNotFoundError:
    print ("I can't seem to find that file, is it in PWD ?")
    sys.exit(1)


def addpass():
    try:
        with open(word_list) as r:
            c.execute("DROP TABLE IF EXISTS easypasswords")
            c.execute('''CREATE TABLE easypasswords (
    	        id integer primary key autoincrement,
    	        password text,
           	    hash text);''')
            print ("Working.....")
            for x in r:
                try:
                    y = x.strip()
                    exe = c.execute("INSERT INTO easypasswords (id, password, hash) VALUES (NULL, ?, NULL)", (str(y),))
                    print("[*] Added " + y + " to the db...")
                    conn.commit()
                except UnicodeDecodeError:
                    pass
    except KeyboardInterrupt:
        conn.close()
        print ("[!] Clean + Exit...")
        sys.exit(1)


addpass()
