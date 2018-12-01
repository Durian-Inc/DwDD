import os

from flask import Flask, render_template, url_for, request, redirect, session
from flask import Flask, flash, abort
from app import app
from flask_sqlalchemy import SQLAlchemy


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        event = {
            'event_name': request.form['eventName'],
            'start_date': request.form['startTime'],
            'end_date': request.form['endTime']
        }
        #add event to table
        redirect_url = '/'+event['event_name']+"-"+event['startDate']
        return redirect(redirect_url, code=302)
    if request.method == 'GET':
        #get all events
        return render_template('listview.html')

@app.route('/<event>', methods = ['POST', 'GET'])
def event_route():
    if not session.get('logged_in'):
        #drunk view
        #if request.method == 'POST':
            #sos
        #if request.method == 'GET':
        #get DDs from event, dd_list = get_dd(event)
        return render_template('drunkview.html')
    else:
        #dd view
        #if request.method == 'POST':
            #add driver to event
        #if request.method == 'GET':
            #get
        return render_template('ddview.html')




@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/SOS')
def sos():
    return render_template('sos.html')


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
