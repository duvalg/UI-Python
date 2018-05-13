#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *

global  uiAlert

def keep_flat(event):       # on click,
    event.widget.config(relief=FLAT) # enforce an option

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


def writeAlert(alert, message):
    alert.config(text=message)
    alert.pack(pady=(25, 0), padx=50)