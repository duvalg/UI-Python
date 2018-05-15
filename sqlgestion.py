# by : Gael Duval

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import MySQLdb

def createDatabase(dbName, connection):         # createDatabase: Create or etablish connection with a database; Return the cursor
    if (connection == "local"):
        db = sqlite3.connect(dbName)
    elif (connection == "distant"):
        host = "localhost"     # host
        user = "root"          # username
        password = ""          # password
        db = MySQLdb.connect(host=host,
        user=user,                                  
        passwd=password,                            
        db=dbName)
    else:
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