import os

from flask import Flask, render_template, url_for, request, redirect, session
from flask import Flask, flash, abort
from app import app
from flask_sqlalchemy import SQLAlchemy
from app.utils import get_all_entries, add_entry_to_db, add_driver_to_event
from app.utils import auth_user, get_event_drivers


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        event = {
            'event_name': request.form['eventName'],
            'start_date': request.form['startTime'],
            'end_date': request.form['endTime']
        }
        add_entry_to_db(event)
        redirect_url = '/'+event['event_name']+"-"+event['startDate']
        return redirect(redirect_url, code=302)
    if request.method == 'GET':
        #get all events
        events = get_all_entries(drivers=False)
        return render_template('listview.html', events)

@app.route('/<event>', methods = ['POST', 'GET'])
def event_route():
    if not session.get('phone_num'):
        #drunk view
        if request.method == 'POST':
        #sos
        return sos()
        if request.method == 'GET':
        #get DDs from event, dd_list = get_dd(event)
        get_event_drivers(event_id)

        return render_template('drunkview.html')
    else:
        #dd view
        #if request.method == 'POST':
        #add driver to event
        #add_driver_to_event()
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
        phone_num = request.form['user']
        pwd = request.form['password']
        if  auth_user(phone_num, pwd) is not None:
            session['phone_num'] = True
            return redirect('/', code=302)
        else:
            return redirect('/login', code=302)
