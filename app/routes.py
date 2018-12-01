import os

from flask import Flask, render_template, url_for, request, redirect, session
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        if  username == 'DD' and password == 'DD':
            session['logged_in'] = True
            return redirect('/', code=302)
        else:
            flash("Invalid login, try again")
            return redirect('/login', code=302)