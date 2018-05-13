#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback
from tkinter.messagebox import *
from tkinter.filedialog import *

# Local scripts
from sqlgestion import *
from ui import *

filename = "sample.txt"

_window = Tk()
_window.title("Databases Manager")
_window.configure(bg="#fafafa")

# Normalize
_window.bind('<Button-1>', keep_flat) # bind the application to left mouse click

db = createDatabase("databases_list.db")
if db == None: # check if database was successfully created or connected
    sys.exit(0)
cursor = getCursor(db)
if cursor == None: # check if getCursor() encountered an error
    sys.exit(0)

def displayList(liste, cursor):            # displayList: display the list of the databases
    i = 1

    liste.delete(0, END)
    cursor.execute('''
    SELECT name 
    FROM databases 
    ORDER BY id 
    DESC
    ''')
    rows = cursor.fetchall()
    for row in rows:
        liste.insert(i, row[0])
        i += 1
    liste.pack()

def insertDatabase(liste, cursor):         # insertDatabase: allow user to get the path of the databases he want to add
    filename = askopenfilename(title="Get file's path",filetypes=[('all files','.*')])

    if (filename):
        checkDuplicate = ('''
        SELECT (1) 
        FROM databases 
        WHERE path = ?
        LIMIT 1
        ''')
        cursor.execute(checkDuplicate, [(filename)])
        if cursor.fetchone():
            print("error while sql request: data already exist [insertDatabase()]")
            writeAlert(alert, "Database already exist !")
        else:
            insertDb = ('''
            INSERT INTO databases(name, path) 
            VALUES(?, ?)
            ''')
            cursor.execute(insertDb, [(os.path.basename(filename)), (filename)])
            db.commit()
            displayList(liste, cursor)
            writeAlert(alert, "Database added")
    
def removeDatabase(liste, cursor, db): # insertDatabase: allow user to get the path of the databases he want to add
    selectedInput = liste.get(ACTIVE)

    if (liste.curselection()):
        if askyesno('Are you sure ?', 'Do you really want to delete this database ?'):
            deleteDatabase = ('''
            DELETE FROM databases 
            WHERE name = ?
            ''')
            cursor.execute(deleteDatabase, [(selectedInput)])
            db.commit()
            writeAlert(alert, "Database deleted")
            displayList(liste, cursor)

#initializing user interface
initMenu(_window)

alert = Label(_window, fg="#282828", bg="#fafafa")
alert.config(text="Welcome to Databases Manager")
alert.pack(pady=(25, 0), padx=50)

liste = Listbox(_window, width=100)
liste.pack(pady=25, padx=50)

insert = Button(_window, 
text="Insert a database", 
height=2, 
width=18, 
fg = "#fff", 
activeforeground = "#fff", 
bg = "#008BD2", 
activebackground = "#005CAA", 
relief=FLAT, 
cursor="hand2", 
command= lambda: insertDatabase(liste, cursor))
insert.pack(padx=50)

delete = Button(_window, 
text="Remove database", 
height=2, 
width=18, 
fg = "#fff", 
activeforeground = "#fff", 
bg = "#fa1a42", 
activebackground = "#c22342", 
relief=FLAT, 
cursor="hand2", 
command= lambda: removeDatabase(liste, cursor, db))
delete.pack(pady=(5, 25), padx=50)

displayList(liste, cursor)

_window.mainloop()
