import sqlite3
import os
from Task import Task

def init(cfg):
    '''
        Set global variables
        Init db if not exist
    '''

    global dbFile
    dbFile = os.path.realpath(os.path.expanduser(
        cfg.get('filesystem', 'database file', fallback = '~/.taskserver.sqlite')
        ))

    if not os.path.exists(dbFile):
        with sqlite3.connect(dbFile) as con:
            con.execute('''
                CREATE TABLE tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deadline CHAR(10),
                    name VARCHAR(255),
                    description TEXT
                )
            ''')

def updateTask(task):
    with sqlite3.connect(dbFile) as con:
        con.execute('''
            UPDATE tasks
            SET deadline = ?,
                name = ?,
                description = ?
            WHERE id = ?
        ''', (
            task.deadline if task.deadline else None,
            task.name,
            task.description,
            task.idx
            ))

def createTask(task):
    with sqlite3.connect(dbFile) as con:
        con.execute('''
            INSERT
            INTO tasks (deadline, name, description)
            VALUES (?, ?, ?)
        ''', (
            task.deadline if task.deadline else None,
            task.name,
            task.description
            ))

def getTask(idx):
    with sqlite3.connect(dbFile) as con:
        cur = con.cursor()

        cur.execute('''
            SELECT *
            FROM tasks
            WHERE id = ?
        ''', (idx,))

        return Task(*cur.fetchone())

def getTasks():
    with sqlite3.connect(dbFile) as con:
        cur = con.cursor()

        cur.execute('''
            SELECT *
            FROM tasks
        ''')

        return list(map(lambda t: Task(*t), cur.fetchall()))
