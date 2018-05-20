# by : Gael Duval

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys, traceback

try:
    # for Python2
    from Tkinter import *
    from tkMessageBox import *
    from tkFileDialog import *
except:
    # for Python3
    from tkinter import *
    from tkinter.messagebox import *
    from tkinter.filedialog import *

# local scripts
from sqlgestion import *
from ui import *
from parser import sqlite3
import parser

root = Tk()
root.title("Databases Manager")
root.configure(bg="#000")

# normalize
root.bind('<Button-1>', keep_flat) # bind the application to left mouse click

# database connection
db = createDatabase("databases_list", "local") # "local" is SQLite3 connexion | "distant" is MySQL connection
if db == None:
    sys.exit(0)
cursor = getCursor(db)
if cursor == None:
    sys.exit(0)

def displayList(lb, cursor): # displayList: display the list of the databases
    i = 1

    # SELECT DATABASES NAME FROM DATABASE
    lb.delete(0, END)
    cursor.execute('''
    SELECT name 
    FROM dbList 
    ORDER BY id 
    DESC
    ''')
    rows = cursor.fetchall()
    for row in rows:
        lb.insert(i, row[0])
        i += 1
    lb.pack()

def insertDatabase(lb, cursor): # insertDatabase: allow user to get the path of the databases he want to add
    filename = askopenfilename(title="Get file's path",filetypes=[
        ('all files','.*'), 
        ('excel documents','*.xlsx')
        ])

    if (filename):

        # GET FILENAME FROM PATH
        dbName = os.path.basename(filename)
        checkDuplicate = ('''
        SELECT (1) 
        FROM dbList 
        WHERE name = ?
        LIMIT 1
        ''')
        
        cursor.execute(checkDuplicate, [(dbName)])
        if cursor.fetchone():
            print("error while sql request: data already exist [insertDatabase()]")
            writeAlert(alert, "Database already exist !")
        else:
            # INSERT NEW DATABASE  
            insertDb = ('''
            INSERT INTO dbList(name, path) 
            VALUES(?, ?)
            ''')
            cursor.execute(insertDb, [(dbName), (filename)])
            db.commit()

            generateDatabase(dbName)
            displayList(lb, cursor)
            writeAlert(alert, "Database added")
    
def exploreDatabase(liste, cursor, db):
    selectedInput = lb.get(ACTIVE)

    if (lb.curselection()):
        
        # SELECT ID FROM DATABASE
        selectId = ('''
        SELECT id 
        FROM dbList
        WHERE name = ?
        LIMIT 1
        ''')
        cursor.execute(selectId, [(selectedInput)])
        rows = cursor.fetchall()
        for row in rows:
            idDb = row[0]
        
        # SELECT DATA FROM SELECTED DATABASE
        selectedDb = sqlite3.connect("output.db")
        selectedCursor = selectedDb.cursor()
        ('''
        SELECT * 
        FROM offre 
        WHERE dbId = ? 
        ORDER BY id
        ''')
        rows = selectedCursor.fetchall()
        for row in rows:
            print(str(row[0]) + " + " + row[1])
        selectedDb.close()



def removeDatabase(lb, cursor, db): # insertDatabase: allow user to get the path of the databases he want to add
    selectedInput = lb.get(ACTIVE)
    dbId = 0

    if (lb.curselection()):
        if askyesno('Are you sure ?', "WARNING\n\nYou're also gonna remove all the associated datas."):
            
            # GET DATABASE'S ID
            getDbId = '''
            SELECT id FROM dbList
            WHERE name = ?
            LIMIT 1
            '''
            cursor.execute(getDbId, [(selectedInput)])
            rows = cursor.fetchall()
            for row in rows:
                dbId = row[0]
                break

            # DELETE DATA FROM THE ASSOCIATED DATABASE
            outputDb = createDatabase("output", "local")
            outputCursor = getCursor(outputDb)

            deleteDatas = '''
            DELETE FROM offre 
            WHERE dbId = ?
            '''
            outputCursor.execute(deleteDatas, [(dbId)])
            outputDb.commit()
            outputDb.close()

            # DELETE DATABASE FROM DATABASES'S LIST
            deleteDatabase = ('''
            DELETE FROM dbList 
            WHERE name = ?
            ''')
            cursor.execute(deleteDatabase, [(selectedInput)])
            db.commit()
            writeAlert(alert, "Database deleted")
            displayList(lb, cursor)

#initializing user interface
initMenu(root)

try:
    photo = PhotoImage(file="img/logo-docaret.png")
except:
    photo = PhotoImage(file="img/logo-docaret.ppm")

canvas = Canvas(root, width=90, height=51, bg="#000", highlightthickness=0, relief="flat")
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack(pady = (25, 0))

alert = Label(root, fg="#fff", bg="#000")
alert.config(text="Welcome to Databases Manager")
alert.pack(pady=(25, 0), padx=50)

lb = Listbox(root, 
selectmode='SINGLE', 
relief="flat", 
bg="#fafafa", 
selectbackground="#fa1a42" ,
bd = 10, 
activestyle = "none", 
width=100
)
lb.pack(pady=25, padx=50)

insert = Button(root, 
text="Insert a new database", 
height=2, 
width=18, 
fg = "#fff", 
activeforeground = "#fff", 
bg = "#008BD2", 
activebackground = "#005CAA", 
relief=FLAT, 
cursor="hand2", 
command= lambda: insertDatabase(lb, cursor))
insert.pack(padx=50)

delete = Button(root, 
text="Explore database", 
height=2, 
width=18, 
fg = "#fff", 
activeforeground = "#fff", 
bg = "#fa1a42", 
activebackground = "#c22342", 
relief=FLAT, 
cursor="hand2", 
command= lambda: exploreDatabase(lb, cursor, db))
delete.pack(pady=(5, 25), padx=50)

delete = Button(root, 
text="Remove database", 
height=2, 
width=18, 
fg = "#fff", 
activeforeground = "#fff", 
bg = "#fa1a42", 
activebackground = "#c22342", 
relief=FLAT, 
cursor="hand2", 
command= lambda: removeDatabase(lb, cursor, db))
delete.pack(pady=(5, 25), padx=50)

displayList(lb, cursor)

root.mainloop()
