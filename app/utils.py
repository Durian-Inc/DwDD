from app.models import DesignatedDriver as DD, Event, db
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


def get_all_entries(drivers=True):
    """
    @purpose: Get a list of json objects for the given entires
    @args:  The table that should be queried
    @returns:   A list of the entries in question as JSON objects
    """
    if drivers:
        driver = {"name": None, "phone": None}
        drivers = []
        for result in DD.query.all():
            driver['name'] = result._driver_name
            driver['number'] = result._driver_phone
            drivers.append(jsonify(driver))
        return drivers
    else:
        local_event = {"name": None, "start_time": None, "end_time": None}
        events = []
        for result in Event.query.all():
            local_event['name'] = result._name
            local_event['start_time'] = result._start_time
            local_event['end_time'] = result._end_time
            local_event['id'] = result._event_id
            events.append(jsonify(local_event))
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
            print(new_event)
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


def get_event_drivers(event_id):
    """
    @purpose: Gets a list of all the drivers that are associated with an event
    @args: The id of the event 
    @return: A list of the drivers in a JSON format
    """ 
    driver = {"name": None, "phone": None}
    drivers = []
    for result in DD.query.filter_by(_driver_curr_event=event_id).all():
        driver['name'] = result._driver_name
        driver['number'] = result._driver_phone
        drivers.append(jsonify(driver))
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
