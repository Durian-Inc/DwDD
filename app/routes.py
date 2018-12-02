import os

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session)
from flask_sqlalchemy import SQLAlchemy
#from twilio.rest import Client
#from twilio.twiml.voice_response import Say, VoiceResponse

from app import app
from app.utils import (add_driver_to_event, add_entry_to_db, auth_user,
                       get_all_entries, get_event_drivers)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        event = {
            'event_name': request.form['eventname'],
            'start_date': request.form['s-time'],
            'end_date': request.form['e-time']
        }
        # id = add_entry_to_db(event)
        redirect_url = '/' + id
        return redirect(redirect_url, code=302)
    if request.method == 'GET':
        #get all events
        #events = get_all_entries(drivers=False)
        events = None
        return render_template('listview.html', events=events)


@app.route('/<event>', methods=['POST', 'GET'])
def event_route(event):
    if not session.get('phone_num'):
        #drunk view
        if request.method == 'POST':
            #sos
            # nums = ['+13145876003', '+13146517436']
            #nums = ['+13145876003']
            #for num in nums:
            #    call(num)
            return redirect("/sos", code=302)
        if request.method == 'GET':
            #get DDs from event, dd_list = get_dd(event)
            # dds = get_event_drivers(event_id)
            dds = None

            return render_template('drunkview.html', dds=dds)
    else:
        #dd view
        #if request.method == 'POST':
        #add driver to event
        #add_driver_to_event()
        #if request.method == 'GET':
        #get
        return render_template('ddview.html')


@app.route('/SOS', methods=['GET'])
@app.route('/sos', methods=['GET'])
def sos():
    return render_template('sos.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


#def call(num):
    # Your Account Sid and Auth Token from twilio.com/console
    #account_sid = 'AC4b362744f0815718c1a3159ddaeeccf4'
    #auth_token = 'c6f53fd9be6781e26005e93f7d1de239'
    #client = Client(account_sid, auth_token)

    #call = client.calls.create(
    #    url=
    #    'https://handler.twilio.com/twiml/EH3d3693b942c9740bae7ec0a24fef443c',
    #    to=num,
    #    from_='+16364342737')

    #print(call.sid)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        print(request.form)
        phone_num = request.form.get('phone')
        pwd = request.form.get('password')
        if auth_user(phone_num, pwd):
            session['phone_num'] = True
            return redirect('/', code=302)
        else:
            return redirect('/login', code=302)
