#! -*- coding: utf-8 -*-
from __future__ import absolute_import

import MySQLdb

from celery import Celery
from celery.signals import worker_init, worker_shutdown

from . import settings

app = Celery('candidate.celery', broker='redis://', backend='redis://')

database = None


@worker_init.connect()
def init_db(**kwargs):
    global database
    database = MySQLdb.connect(host='localhost',
                               db=settings.DB_NAME,
                               user=settings.DB_LOGIN,
                               passwd=settings.DB_PASSWORD)
    database.autocommit(True)
    c = database.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS candidate (
            uid INTEGER AUTO_INCREMENT PRIMARY KEY,
            sid INTEGER DEFAULT 0,
            site_id INTEGER DEFAULT 0,
            cid INTEGER DEFAULT 15,
            real_cid INTEGER DEFAULT 0,
            ip INTEGER DEFAULT 0,
            name VARCHAR(256) NOT NULL,
            email VARCHAR(256) NOT NULL UNIQUE,
            mobile VARCHAR(256) DEFAULT '',
            code1 VARCHAR(256) DEFAULT 'webresume',
            code2 VARCHAR(256) DEFAULT '',
            level1 INTEGER DEFAULT 0,
            level2 INTEGER DEFAULT 0,
            time INTEGER DEFAULT 0,
            status INTEGER DEFAULT 0,
            clear INTEGER DEFAULT 1
         ) ENGINE=MyISAM, CHARSET='utf8';
        """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS last_processed (
            industry INTEGER PRIMARY KEY,
            pageno INTEGER NOT NULL
        ) ENGINE=MyISAM, CHARSET='utf8';
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS stopped (
            industry INTEGER PRIMARY KEY,
            stoped DATETIME,
            pageno INTEGER NOT NULL
        ) ENGINE=MyISAM, CHARSET='utf8';
    """)
    c.execute("SET SESSION tx_isolation = 'READ-COMMITTED'")
    c.execute("SET GLOBAL concurrent_insert = 2")
    c.close()


@worker_shutdown.connect()
def close_db(**kwargs):
    database.close()

@app.task
def save_user(name, email):

    c = database.cursor()
    try:
        c.execute("INSERT INTO candidate (name,email) VALUES (%s, %s)", (name, email))
    except MySQLdb.Error as e:
        pass
    finally:
        c.close()

@app.task
def save_last_processed(indst, page):
    c = database.cursor()
    try:
        c.execute("REPLACE DELAYED INTO last_processed VALUES (%s, %s)", (indst, page))
    except MySQLdb.Error as e:
        pass
    finally:
        c.close()

@app.task
def save_stopped(indst, at, page):
    c = database.cursor()
    try:
        c.execute("REPLACE DELAYED INTO stopped VALUES (%s, %s, %s)", (indst, at, page))
    except MySQLdb.Error as e:
        pass
    finally:
        c.close()



@app.task
def get_last_processed():
    c = database.cursor()
    result = None
    try:
        c.execute("SELECT * FROM last_processed")
        result = c.fetchall()
    except MySQLdb.Error as e:
        pass
    finally:
        c.close()
    return result






