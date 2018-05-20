# by : Gael Duval

#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    # for Python2
    from Tkinter import *
except:
    # for Python3
    from tkinter import *

# Local scripts
from parser import *

global  uiAlert

def keep_flat(event):       # on click,
    event.widget.config(relief=FLAT) # enforce an option

def initMenu(root):                      # initMenu: init interface's menu
    menubar = Menu(root)

    tools = Menu(menubar, tearoff=0)
    tools.add_command(label="Insert a database", command= lambda: insertDatabase(liste, cursor))
    tools.add_command(label="Remove database", command= lambda: removeDatabase(liste, cursor, db))
    tools.add_separator()
    # tools.add_command(label="Exporting database", command= generateDatabase)
    tools.add_separator()
    tools.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Tools", menu=tools)
    root.config(menu=menubar)

def writeAlert(alert, message):
    alert.config(text=message)
    alert.pack(pady=(25, 0), padx=50)