#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3                      # needed to connect the program to a SQL database

def createDatabase(dbName):         # createDatabase: Create or etablish connection with a database; Return the cursor
    try:
        db = sqlite3.connect(dbName)
    except:
        return None
    return db
        

def getCursor(db):
    try:
        _cursor = db.cursor()
        _cursor.execute('''
        CREATE TABLE IF NOT EXISTS databases(
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    VARCHAR(30)     NOT NULL,
            path    VARCHAR(100)    NOT NULL);
        ''')
    except:
        return None
    return _cursor