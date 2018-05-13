#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback
try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
    from tkMessageBox import *   ## notice capitalized T in Tkinter 
    from tkFileDialog import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
    from tkinter.messagebox import *
    from tkinter.filedialog import *

# Local scripts
from sqlgestion import *

filename = "sample.txt"

_window = Tk()

db = createDatabase("databases_list.db")
if db == None: # check if database was successfully created or connected
    sys.exit(0)
cursor = getCursor(db)
if cursor == None: # check if getCursor() encountered an error
    sys.exit(0)

# def readfile(dbList, liste):
#     with open(filename, "r") as fd:
#         line = fd.readline()

#         while line:
#             dbList.append(line.strip())
#             line = fd.readline()
#     displayList(dbList, liste)

# def rewriteFile(dbList, ignored):
#     i = 0
#     fd = open(filename, "w")
    
#     for line in dbList:
#         if (i != ignored):
#             fd.write(line + "\n")
#         i += 1

def displayList(liste, cursor):            # displayList: display the list of the databases
    i = 1

    liste.delete(0, END)
    cursor.execute('SELECT name FROM databases ORDER BY id DESC')
    rows = cursor.fetchall()
    for row in rows:
        liste.insert(i, row[0])
        i += 1
    liste.pack()

def insertDatabase(liste, cursor):         # insertDatabase: allow user to get the path of the databases he want to add
    filename = askopenfilename(title="Get file's path",filetypes=[('all files','.*')])

    if (filename):
        insertDb = ('''
        INSERT INTO databases(name, path) VALUES(?, ?)
        ''')
        cursor.execute(insertDb, [(os.path.basename(filename)), (filename)])
        db.commit()
    displayList(liste, cursor)
    
def removeDatabase(liste, cursor, db):         # insertDatabase: allow user to get the path of the databases he want to add
    selectedInput = liste.get(ACTIVE)

    if (selectedInput):
        if askyesno('Are you sure ?', 'Do you really want to delete this database ?'):
            deleteDatabase = ("DELETE FROM databases WHERE name = ?")
            cursor.execute(deleteDatabase, [(selectedInput)])
            db.commit()
            displayList(liste, cursor)

def initMenu(_window):                      # initMenu: init interface's menu
    menubar = Menu(_window)

    tools = Menu(menubar, tearoff=0)
    tools.add_command(label="Insert a database", command= lambda: insertDatabase(liste, cursor))
    tools.add_command(label="Remove database", command= lambda: removeDatabase(liste, cursor, db))
    tools.add_separator()
    tools.add_command(label="Exporting database")
    tools.add_separator()
    tools.add_command(label="Exit", command=_window.quit)
    menubar.add_cascade(label="Tools", menu=tools)
    _window.config(menu=menubar)

initMenu(_window)

# Add a database (button)
bouton=Button(_window, text="Insert a database", command= lambda: insertDatabase(liste, cursor)).pack(pady=25, padx=50)

# Initializing databases (listBox)
liste = Listbox(_window, width=100)
liste.pack(padx=50)

# Delete database (button)
bouton=Button(_window, text="Remove database", command= lambda: removeDatabase(liste, cursor, db)).pack(pady=25, padx=50)

# Initialisation read
# readfile(dbList, liste)
displayList(liste, cursor)

_window.mainloop()
