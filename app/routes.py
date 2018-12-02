import os
from datetime import datetime

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session)
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client

from app import app
from app.utils import (add_driver_to_event, add_entry_to_db, auth_user,
                       get_all_entries, get_event_drivers)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        event = {
            'event_name': request.form['eventname'],
            'start_time': request.form['s-time'],
            'end_time': request.form['e-time']
        }
        eventid = add_entry_to_db(event)
        if eventid != 0:
            redirect_url = '/' + str(eventid)
        else:
            flash("Failed to create event", "danger")
            redirect_url = '/'
        return redirect(redirect_url, code=302)
    if request.method == 'GET':
        #get all events
        resp = get_all_entries(drivers=False)
        now = datetime.now()
        relevant = [x for x in resp if x['end_time'] > now]
        events = {
            "now": [x for x in relevant if x['start_time'] < now],
            "upcoming": [x for x in relevant if x['start_time'] > now]
        }
        return render_template('listview.html', events=events)


@app.route('/<event_id>', methods=['POST', 'GET'])
def event_route(event_id):
    if not session.get('phone_num'):
        #drunk view
        if request.method == 'POST':
            #sos
            # nums = ['+13145876003', '+13146517436']
            nums = ['+13145876003']
            for num in nums:
                call(num)
            return redirect("/sos", code=302)
        if request.method == 'GET':
            #get DDs from event, dd_list = get_dd(event)
            dds = get_event_drivers(event_id)
            return render_template('drunkview.html', dds=dds)
    else:
        #dd view
        if request.method == 'POST':
            return "oops"
        if request.method == 'GET':
            #add driver to event
            add_driver_to_event(session.get('phone_num'), event_id)
            #get
            return render_template('ddview.html')


@app.route('/SOS', methods=['GET'])
@app.route('/sos', methods=['GET'])
def sos():
    return render_template('sos.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


def call(num):
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC4b362744f0815718c1a3159ddaeeccf4'
    auth_token = 'c6f53fd9be6781e26005e93f7d1de239'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url=
        'https://handler.twilio.com/twiml/EH3d3693b942c9740bae7ec0a24fef443c',
        to=num,
        from_='+16364342737')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        phone_num = request.form.get('phone')
        pwd = request.form.get('password')
        if auth_user(phone_num, pwd):
            session['phone_num'] = phone_num
            flash("Logged in!", "success")
            return redirect('/', code=302)
        else:
            flash("Failed to login, try again", "danger")
            return redirect('/login', code=302)


@app.route('/logout', methods=['GET'])
def logout():
    session['phone_num'] = None
    flash("Logged out", "success")
    return redirect('/', code=302)
