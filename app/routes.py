import os

from app import app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


@app.route('/')
def hello():
    return render_template('listview.html')


@app.route('/a')
def bonk():
    return render_template('drunkview.html')


@app.route('/d')
def bink():
    return render_template('ddview.html')


@app.route('/login')
def log():
    return render_template('login.html')
