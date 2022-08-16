#!/bin/python

import flask
from configparser import ConfigParser
from waitress import serve
import sys
import os
import re
import logics
from Task import Task

def usage():
    print('Usage: {} run'.format(sys.argv[0]))

if len(sys.argv) != 2:
    usage()
    exit(1)

if sys.argv[1] != 'run':
    usage()
    exit(1)

cfg = ConfigParser()
cfg.SECTCRE = re.compile(r'\[ *(?P<header>[^]]+?) *\]')
cfg.read(os.path.expanduser('~/.taskserverrc'))

logics.init(cfg)

app = flask.Flask(__name__,
    template_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates'))

@app.route('/')
def index():
    return flask.redirect('/tasklist')

@app.route('/tasklist')
def tasklist():
    return flask.render_template(
        'tasklist.j2',
        tasks = logics.getTasks()
        )

@app.route('/task', methods = ['GET', 'POST'])
def createTask():
    if flask.request.method == 'GET':
        return flask.render_template(
            'task.j2',
            task = Task.fictive())

    if 'save' in flask.request.form:
        task = Task(-1,
            flask.request.form['deadline'],
            flask.request.form['description']
            )

        logics.createTask(task)

    return flask.redirect('/tasklist')

@app.route('/task/<int:idx>', methods=['GET', 'POST'])
def editTask(idx):
    if flask.request.method == 'GET':
        return flask.render_template(
            'task.j2',
            task = logics.getTask(idx))

    if 'save' in flask.request.form:
        task = Task(idx,
            flask.request.form['deadline'],
            flask.request.form['description']
            )

        logics.updateTask(task)

    return flask.redirect('/tasklist')

@app.route('/deleteTask/<int:idx>', methods=['POST'])
def deleteTask(idx):
    logics.deleteTask(idx)

    return flask.redirect('/tasklist')

if __name__ == '__main__':
    serve(
        app,
        host = '0.0.0.0',
        port = cfg.get('network', 'port', fallback=5000)
        )
