'''
Utility functions for the application
'''
from datetime import datetime
from functools import wraps

from flask import redirect, request, session, url_for

from app.models import DesignatedDriver as DD
from app.models import Event, db
from twilio.rest import Client


def get_all_entries(drivers=True):
    """
    @purpose: Get a list of json objects for the given entires
    @args:  The table that should be queried
    @returns:   A list of the entries in question as JSON objects
    """
    if drivers:
        drivers = []
        for result in DD.query.all():
            driver = {"name": None, "phone": None}
            driver['name'] = result._driver_name
            driver['number'] = result._driver_phone
            drivers.append(driver)
        return drivers
    else:
        events = []
        for result in Event.query.all():
            local_event = {"name": None, "start_time": None, "end_time": None}
            local_event['name'] = result._name
            datetime_object = datetime.strptime(result._start_time,
                                                '%m/%d/%Y %I:%M %p')
            local_event['start_time'] = datetime_object
            datetime_object = datetime.strptime(result._end_time,
                                                '%m/%d/%Y %I:%M %p')
            local_event['end_time'] = datetime_object
            local_event['id'] = result._event_id
            events.append(local_event)
        return events


def add_entry_to_db(entry, is_event=True):
    """
    @purpose:   Adds an entry to the database
    @args:  The entry as a dictionary, a bool to tell if it is an event
    @return:    True / False based on the commit to the database
    """
    if is_event:
        try:
            entry_id = len(Event.query.all())
            if entry_id == 0:
                entry_id = 1
            else:
                entry_id += 1
            new_event = Event(entry['event_name'], entry['start_time'],
                              entry['end_time'], entry_id)
            db.session.add(new_event)
            db.session.commit()
            return entry_id
        except:
            return 0
    else:
        try:
            new_driver = DD(entry['name'], entry['pwd'], entry['phone'])
            db.session.add(new_driver)
            db.session.commit()
            return len(new_driver)
        except:
            return 0


def add_driver_to_event(driver_phone, event_id):
    """
    @purpose:   Links a driver to an event
    @args:  Driver's phone number, the id of the event
    @return:    True / False based on the update to the database
    """
    try:
        driver = DD.query.filter_by(_driver_phone=driver_phone).first()
        driver._driver_curr_event = event_id
        db.session.commit()
        return True
    except:
        return False


def change_driver_state(driver_phone):
    """
    @purpose: Changes the state of the driver's availability
    @args: Driver's phone number 
    @returns: True / False based on if the commit went well
    """
    try:
        driver = DD.query.filter_by(_driver_phone=driver_phone).first()
        driver._driver_is_available = not (driver._driver_is_available)
        db.session.commit()
        return True
    except:
        return True


def get_driver(driver_phone):
    """
    @purpose: Changes the state of the driver's availability
    @args: Driver's phone number 
    @returns: True / False based on if the commit went well
    """
    try:
        result = DD.query.filter_by(_driver_phone=driver_phone).first()
        driver = {"name": None, "phone": None}
        driver['name'] = result._driver_name
        driver['number'] = result._driver_phone
        driver['available'] = result._driver_is_available

        return driver
    except:
        return None


def get_event_drivers(event_id):
    """
    @purpose: Gets a list of all the drivers that are associated with an event
    @args: The id of the event 
    @return: A list of the drivers in a JSON format
    """
    drivers = []
    for result in DD.query.filter_by(_driver_curr_event=event_id).all():
        driver = {"name": None, "phone": None, "available": None}
        driver['name'] = result._driver_name
        driver['phone'] = result._driver_phone
        driver['available'] = result._driver_is_available
        drivers.append(driver)
    return drivers


def auth_user(phone, pwd):
    """
    @purpose: Authenticate a user with their phone and their password.
    @args: The user's username. The password.
    @return: True or false if the user is validated
    """
    result = DD.query.filter_by(_driver_phone=phone).first()
    if result is not None and result._driver_password == pwd:
        return True
    else:
        return False
    return False


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('phone_num'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def call(num):
    account_sid = ''  # Removed and key deleted
    auth_token = ''  # Removed and key deleted

    twiml_link = ''
    twilio_number = ''

    if account_sid and auth_token and twiml_link and twilio_number:
        client = Client(account_sid, auth_token)
        call = client.calls.create(url=twiml_link, to=num, from_=twilio_number)
