# by : Gael Duval

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import MySQLdb

def createDatabase(dbName, connection):         # createDatabase: Create or etablish connection with a database; Return the cursor
    if (connection == "local"):
        db = sqlite3.connect(dbName + ".db")
    elif (connection == "distant"):
        host = "localhost"              # host
        user = "root"                   # username
        password = "blackrose"          # password
        db = MySQLdb.connect(host=host,
        user=user, 
        passwd=password, 
        db=dbName)
    else:
        return None
    return db
        

def getCursor(db):
    _cursor = db.cursor()
    _cursor.execute('''
    CREATE TABLE IF NOT EXISTS dbList(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(40) NOT NULL,
        path VARCHAR(100) NOT NULL);
    ''')

    _cursor.execute('''
    CREATE TABLE IF NOT EXISTS offre(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client                  VARCHAR(40)     NOT NULL,
        reference_wp            VARCHAR(40)     NOT NULL,
        numero_ap               VARCHAR(40)     NOT NULL,
        division                VARCHAR(40)     NOT NULL,
        date_envoi              VARCHAR(40)     NOT NULL,
        date_limite             VARCHAR(40)     NOT NULL,
        postes_dispo            VARCHAR(40)     NOT NULL,
        date_debut              VARCHAR(40)     NOT NULL,
        duree                   VARCHAR(40)     NOT NULL,
        fonction                VARCHAR(100)    NOT NULL,
        region                  VARCHAR(100)    NOT NULL,
        code_gcm                VARCHAR(40)     NOT NULL,
        remuneration            VARCHAR(40)     NOT NULL,
        domaine_technique       VARCHAR(40)     NOT NULL,
        secteur_activite        VARCHAR(40)     NOT NULL,
        seniorite               VARCHAR(40)     NOT NULL,
        point_important         VARCHAR(40)     NOT NULL,
        descriptif_mission      VARCHAR(255)    NOT NULL,
        preembauche             VARCHAR(40)     NOT NULL,
        critere_a               VARCHAR(40)     NOT NULL,
        critere_b               VARCHAR(40)     NOT NULL,
        critere_c               VARCHAR(40)     NOT NULL,
        descriptif_joint        VARCHAR(40)     NOT NULL,
        operationnel_a          VARCHAR(40)     NOT NULL,
        operationnel_b          VARCHAR(40)     NOT NULL,
        operationnel_c          VARCHAR(40)     NOT NULL,
        societe                 VARCHAR(40)     NOT NULL,
        nom                     VARCHAR(40)     NOT NULL,
        email                   VARCHAR(40)     NOT NULL,
        telephone               VARCHAR(40)     NOT NULL,
        dbId                    VARCHAR(100)    NOT NULL);
    ''')
    return _cursor