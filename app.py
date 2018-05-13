#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback
try:
    # for Python2
    from Tkinter import *
    from tkMessageBox import *
    from tkFileDialog import *
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter.messagebox import *
    from tkinter.filedialog import *

# local scripts
from sqlgestion import *
from ui import *

filename = "sample.txt"

root = Tk()
root.title("Databases Manager")
root.configure(bg="#000")

# normalize
root.bind('<Button-1>', keep_flat) # bind the application to left mouse click

# database connection
db = createDatabase("databases_list.db", "local") # "local" | "distant"
if db == None:
    sys.exit(0)
cursor = getCursor(db)
if cursor == None:
    sys.exit(0)

def displayList(lb, cursor): # displayList: display the list of the databases
    i = 1

    lb.delete(0, END)
    cursor.execute('''
    SELECT name 
    FROM databases 
    ORDER BY id 
    DESC
    ''')
    rows = cursor.fetchall()
    for row in rows:
        lb.insert(i, row[0])
        i += 1
    lb.pack()

def insertDatabase(lb, cursor): # insertDatabase: allow user to get the path of the databases he want to add
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
            displayList(lb, cursor)
            writeAlert(alert, "Database added")
    
def removeDatabase(lb, cursor, db): # insertDatabase: allow user to get the path of the databases he want to add
    selectedInput = lb.get(ACTIVE)

    if (lb.curselection()):
        if askyesno('Are you sure ?', 'Do you really want to delete this database ?'):
            deleteDatabase = ('''
            DELETE FROM databases 
            WHERE name = ?
            ''')
            cursor.execute(deleteDatabase, [(selectedInput)])
            db.commit()
            writeAlert(alert, "Database deleted")
            displayList(lb, cursor)

#initializing user interface
initMenu(root)

photo = PhotoImage(file="img/logo-docaret.png")

canvas = Canvas(root, width=90, height=51, bg="#000", highlightthickness=0, relief="flat")
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack(pady = (25, 0))

alert = Label(root, fg="#fff", bg="#000")
alert.config(text="Welcome to Databases Manager")
alert.pack(pady=(25, 0), padx=50)

lb = Listbox(root, 
selectmode='BROWSE', 
relief="flat", 
bg="#fafafa", 
selectbackground="#fa1a42" ,
bd = 10, 
activestyle = "none", 
width=100
)
lb.pack(pady=25, padx=50)

insert = Button(root, 
text="Insert a database", 
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
