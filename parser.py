# by : Hadrien Cornier

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""       
import xlrd
import datetime  
import sqlite3

def generateDatabase(dbName):
    conn = sqlite3.connect('data-manager.db')
    c = conn.cursor()

    def cellval(cell, datemode):
        if cell.ctype == xlrd.XL_CELL_DATE:
            datetuple = xlrd.xldate_as_tuple(float(cell.value), datemode)
            if datetuple[3:] == (0, 0, 0):
                return datetime.date(datetuple[0], datetuple[1], datetuple[2])
            return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
        if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
        if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
        return cell.value


    def nombre_de_tableaux():
        n=0
        n=((r-45)/38)*2-(1-(sheet.cell_type(r-1, 4)))
        return n

    def lc(a,b,c):
        L=[]
        for i in range(a,b):
            L=L+[sheet.cell(i,c)]
        return L
        
    def xstr(s):
        return '' if s is None else str(s)

    def esp(s):
        s=xstr(s)
        r=""
        for a in range(0,len(s)):
            if s[a]=="'":
                r+="_"
                continue
            if s[a]=="/":
                r+="|"
                continue
            if s[a]=="-":
                r+="_"
                continue
            if ((s[a]=="(") or (s[a]==")")):
                r+=''
            else:
                r+=s[a]
        if r=="" : return r
        i =0
        while i<len(r) and (r[-i]==" " or r[-i]=="_"):
            i=i+1
        if i==0 :return r
        return r[:-i]


    def construct(r, dbId):
        
        n=int((r-45)/38)
        for i in range(0,n+1):
            L=lc(14+38*i,14+38*i+22,2)+lc(14+38*i+23,14+38*i+26,2)+lc(14+38*i+27,14+38*i+31,2)
            L1=["System_GIE"]+[cellval(c, book.datemode) for c in L]

            L11=[esp(i) for i in L1]

            A=["'"+i+"'" for i in L11]
            vals=' , '.join(A)
            c.execute('insert into offre values (NULL,' + vals + ' , ' + dbId + ')')
            conn.commit()
            
            if (sheet.cell_type(14+38*i, 4)!=0):
                L=lc(14+38*i,14+38*i+22,5)+lc(14+38*i+23,14+38*i+26,5)+lc(14+38*i+27,14+38*i+31,5)
                L2=["System_GIE"]+[cellval(c, book.datemode) for c in L]
                L22=[esp(i) for i in L2]
                B=["'"+i+"'" for i in L22]
                vals=' , '.join(B)
                c.execute('insert into offre values (NULL,' + vals + ' , ' + dbId + ')')
                conn.commit()
        return 

    def ExcelAP(path):
        book = xlrd.open_workbook(file_contents=open(path, 'rb').read())
        sheet = book.sheet_by_name('AP')
        r=sheet.nrows
        construct(r)
        return

    # Bridge UI - Parser
    with sqlite3.connect('data-manager.db') as db:
        dbCursor = db.cursor()

        getDatabase = '''
            SELECT path, id
            FROM dbList 
            WHERE name = ? 
            '''
        dbCursor.execute(getDatabase, [(dbName)])
        rows = dbCursor.fetchall()

        print("Generating database...")
        for row in rows:
            print("Using " + row[0])
            book = xlrd.open_workbook(file_contents=open(row[0], 'rb').read())
            sheet = book.sheet_by_name('AP')
            r=sheet.nrows
            construct(r, str(row[1]))
        print("Database generated")

    conn.close()