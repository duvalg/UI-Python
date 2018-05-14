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

def generateDatabase():
    conn = sqlite3.connect('output.db')
    c = conn.cursor()
    keys=[]

    keys=keys+["Client"]   
    keys=keys+["Référence_WP"]  
    keys=keys+["Numero_AP"]
    keys=keys+["Division"]
    keys=keys+["Date_envoi"]
    keys=keys+["Date_limite"]
    keys=keys+["Nombre_de_postes_à_pourvoir"]
    keys=keys+["Date_de_début"]
    keys=keys+["Durée"]
    keys=keys+["Fonction"]
    keys=keys+["Region"]
    keys=keys+["Code_GCM"]
    keys=keys+["Remunération"]
    keys=keys+["Domaine_technique"]
    keys=keys+["Secteur_activité"]
    keys=keys+["Séniorité"]
    keys=keys+["Point_important"]
    keys=keys+["Descriptif_mission"]
    keys=keys+["Préembauche"]
    keys=keys+["Critère_A"]
    keys=keys+["Critère_B"]
    keys=keys+["Critère_C"]
    keys=keys+["Descriptif_joint"]
    keys=keys+["Operationnel_A "]
    keys=keys+["Operationnel_B "]
    keys=keys+["Operationnel_C "]
    keys=keys+["Société"]
    keys=keys+["Nom"]
    keys=keys+["Email"]
    keys=keys+["Téléphone"]

    K=""
    for i in range(len(keys)):
        K=K+keys[i] 
        K=K+" TEXT , "
    K=K[:-2]
    # print(K)
    c.execute("DROP TABLE IF EXISTS offre")
    c.execute("CREATE TABLE offre(id INTEGER PRIMARY KEY, "+K+")")
    conn.commit()

    #def main():
    #    ExcelAP(r"C:\Users\PC\Documents\project docaret\ATOS_AP_12042018.xlsx");
    #    ExcelAP(r"C:\Users\PC\Documents\project docaret\ATOS_AP_28032018 - Partie 1.xlsx");
    #    ExcelAP(r"C:\Users\PC\Documents\project docaret\ATOS_AP_28032018 - Partie 2.xlsx");

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
        #sheet.cell_type(m,p)=0 si c'est vide et 1 sinon
        n=0
        n=((r-45)/38)*2-(1-(sheet.cell_type(r-1, 4)))
        #if (sheet.cell(nrows,4)=="")
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
    #        if s[a]!=" ":
            if ((s[a]=="(") or (s[a]==")")):
                    r+=''
            else:
                    r+=s[a]
    #        else :
    #            r+="_"
        if r=="" : return r
        i =0
        while i<len(r) and (r[-i]==" " or r[-i]=="_"):
                i=i+1
        if i==0 :return r
    #    if r[-1]==" ": return r[:-1]
        return r[:-i]


    def construct(r):
        
        n=int((r-45)/38)
        # print("n=" + str(n))
        #problème parité
        for i in range(0,n+1):
    #          print("i="+str(i))
    #          print(14+38*i)
    #          print(sheet.cell_type(14+38*i, 2))
    #          print(sheet.cell_type(14+38*i+22, 2))
    #          print(sheet.cell_type(14+38*i+23, 2))
    #          print(sheet.cell_type(14+38*i+26, 2))
    #          print(sheet.cell_type(14+38*i+27, 2))
    #          print(sheet.cell_type(14+38*i+31, 2))
            
            L=lc(14+38*i,14+38*i+22,2)+lc(14+38*i+23,14+38*i+26,2)+lc(14+38*i+27,14+38*i+31,2)
            L1=["System_GIE"]+[cellval(c, book.datemode) for c in L]

            L11=[esp(i) for i in L1]

            A=["'"+i+"'" for i in L11]
            vals=' , '.join(A)
            # (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            # print(vals)
            c.execute('insert into offre values (NULL,'+vals+')')
            #c.execute('insert into offre values ('+vals+')')
            conn.commit()
            
            if (sheet.cell_type(14+38*i, 4)!=0):
                L=lc(14+38*i,14+38*i+22,5)+lc(14+38*i+23,14+38*i+26,5)+lc(14+38*i+27,14+38*i+31,5)
                L2=["System_GIE"]+[cellval(c, book.datemode) for c in L]
                L22=[esp(i) for i in L2]
                B=["'"+i+"'" for i in L22]
                vals=' , '.join(B)
                c.execute('insert into offre values (NULL,'+vals+')')
                conn.commit()
        return 

    def ExcelAP(path):
        book = xlrd.open_workbook(file_contents=open(path, 'rb').read())
        sheet = book.sheet_by_name('AP')
        r=sheet.nrows
        construct(r)
        return

    # Bridge UI - Parser
    with sqlite3.connect('databases_list.db') as db:
        dbCursor = db.cursor()

        dbCursor.execute('''
            SELECT path 
            FROM databases 
            ''')
        rows = dbCursor.fetchall()

        print("Generating database...")
        for row in rows:
            print("Using " + row[0])
            book = xlrd.open_workbook(file_contents=open(row[0], 'rb').read())
            sheet = book.sheet_by_name('AP')
            r=sheet.nrows
            construct(r)
        print("Database generated")

    conn.close()