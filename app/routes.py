'''
Includes all routes used in the application
'''
from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for

from app import app
from app.utils import (add_driver_to_event, add_entry_to_db, auth_user, call,
                       change_driver_state, get_all_entries, get_driver,
                       get_event_drivers, login_required)


@app.route('/', methods=['POST', 'GET'])
def events():
    if request.method == 'POST':
        event = {
            'event_name': request.form['eventname'],
            'start_time': request.form['s-time'],
            'end_time': request.form['e-time']
        }
        event_id = add_entry_to_db(event)
        if event_id != 0:
            flash("Successfully created event!", "success")
            return redirect(url_for('event', event_id=event_id))
        else:
            flash("Failed to create event", "danger")
            return redirect(url_for('events'))
    if request.method == 'GET':
        resp = get_all_entries(drivers=False)
        now = datetime.now()

        relevant = [x for x in resp if x['end_time'] > now]
        events = {
            "now": [x for x in relevant if x['start_time'] < now],
            "upcoming": [x for x in relevant if x['start_time'] > now]
        }
        return render_template('listview.html', events=events)


@app.route('/events/<event_id>', methods=['POST', 'GET'])
def event(event_id):
    if not session.get('phone_num'):
        if request.method == 'GET':
            dds = get_event_drivers(event_id)
            return render_template('drunkview.html', dds=dds)

        if request.method == 'POST':
            dds = get_event_drivers(event_id)
            nums = [x['phone'] for x in dds if x['available']]
            for num in nums:
                call(num)
            return redirect(url_for('sos'))

    else:
        if request.method == 'GET':
            add_driver_to_event(session.get('phone_num'), event_id)

        if request.method == 'POST':
            change_driver_state(session.get('phone_num'))

        driver = get_driver(session.get('phone_num'))

        return render_template('ddview.html', me=driver)


@app.route('/sos', methods=['GET'])
def sos():
    return render_template('sos.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


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
            return redirect(url_for('events'))
        else:
            flash("Failed to login, try again.", "danger")
            return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    add_driver_to_event(session.get('phone_num'), 0)
    session['phone_num'] = None

    flash("Logged out", "success")
    return redirect(url_for('events'))
