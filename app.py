#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

import sqlite3                      # needed to connect the program to a SQL database

filename = "sample.txt"             # filename: path to the text file that contains databases's path

_window = Tk()
_dbList = []

# File reading-writing gestion
def readfile(_dbList, liste):
    with open(filename, "r") as fd:
        fd.seek(0)
        line = fd.readline()

        while line:
            _dbList.append(line.strip())
            print("file input : " + line.strip()) # debug
            line = fd.readline()
        print("\n")
    displayList(_dbList, liste)

def rewriteFile(_dbList, ignored):
    i = 0
    fd = open(filename, "w")
    
    for line in _dbList:
        if (i != ignored):
            print("rewriteFile = " + line)
            fd.write(line + "\n")
        i += 1

def displayList(_dbList, liste):            # displayList: display the list of the databases
    i = 1

    liste.delete(0, END)
    for path in _dbList:
        print("displayList = " + path)
        liste.insert(i, path)
    print("\n")
    liste.pack()

def insertDatabase(_dbList, liste):         # insertDatabase: allow user to get the path of the databases he want to add
    filename = askopenfilename(title="Get file's path",filetypes=[('all files','.*')])

    if (filename):
        _dbList.append(filename)
        rewriteFile(_dbList, -1)
        del _dbList[:]
        readfile(_dbList, liste)
    
def removeDatabase(liste, _dbList):  # insertDatabase: allow user to get the path of the databases he want to add
    selectedInput = liste.curselection()
    
    if (selectedInput):
        if askyesno('Are you sure ?', 'Do you really want to delete this database ?'):
            index = selectedInput[0]    # get the index of the undesired data
            rewriteFile(_dbList, index)
            del _dbList[:]
            readfile(_dbList, liste)

def initMenu(_window):               # initMenu: init interface's menu
    menubar = Menu(_window)

    tools = Menu(menubar, tearoff=0)
    tools.add_command(label="Insert a database", command= lambda: insertDatabase(_dbList, liste))
    tools.add_command(label="Remove database", command= lambda: insertDatabase(_dbList, liste))
    tools.add_separator()
    tools.add_command(label="Exporting database")
    tools.add_separator()
    tools.add_command(label="Exit", command=_window.quit)
    menubar.add_cascade(label="Tools", menu=tools)
    _window.config(menu=menubar)

initMenu(_window)

# Add a database (button)
bouton=Button(_window, text="Insert a database", command= lambda: insertDatabase(_dbList, liste)).pack(pady=25, padx=50)

# Initializing databases (listBox)
liste = Listbox(_window, width=100)
liste.pack(padx=50)

# Delete database (button)
bouton=Button(_window, text="Remove database", command= lambda: removeDatabase(liste, _dbList)).pack(pady=25, padx=50)

# Initialisation read
readfile(_dbList, liste)

_window.mainloop()