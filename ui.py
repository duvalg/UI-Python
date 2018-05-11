#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

global  window
global  dbList
global  liste

window = Tk()
dbList = []

def displayList(dbList):            # displayList: display the list of the databases
    i = 1

    liste.delete(0, END)
    for path in dbList:
        liste.insert(i, path)
        i += 1
    liste.pack()

def insertDatabase(dbList):         # insertDatabase: allow user to get the path of the databases he want to add
    filename = askopenfilename(title="Get file's path",filetypes=[('all files','.*')])
    dbList.append(filename)
    displayList(dbList)
    
def removeDatabase(liste, dbList):  # insertDatabase: allow user to get the path of the databases he want to add
    selectedInput = liste.curselection()
    
    if (selectedInput):
        index = selectedInput[0]
        liste.delete(selectedInput)
        del dbList[index]

def initMenu(window):               # initMenu: init interface's menu
    menubar = Menu(window)

    tools = Menu(menubar, tearoff=0)
    tools.add_command(label="Insert a database", command= lambda: insertDatabase(dbList))
    tools.add_separator()
    tools.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="Tools", menu=tools)
    window.config(menu=menubar)

initMenu(window)

# Add a database (button)
bouton=Button(window, text="Insert a new database", command= lambda: insertDatabase(dbList)).pack(pady=25, padx=50)

# Initializing databases (listBox)
liste = Listbox(window, width=100)
liste.pack(padx=50)

# Delete database (button)
bouton=Button(window, text="Delete database", command= lambda: removeDatabase(liste, dbList)).pack(pady=25, padx=50)

window.mainloop()