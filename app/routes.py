import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
