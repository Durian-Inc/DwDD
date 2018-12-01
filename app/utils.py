from app.models import DesignatedDriver as DD, Event
from flask import jsonify


def get_all_entries(drivers=True):
    """
    @purpose: Get a list of json objects for the given entires
    @args:  The table that should be queried
    @returns:   None
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
    @purpose:
    @args: 
    @return:
    """
    if is_event:
        try:
            new_event = Event(entry['name'], entry['start_time'], entry['end_time'], entry['id'])
            db.session.add(new_event)
            db.session.commit()
            return True
        except:
            return False
    else:
        try:
            new_driver = DD(entry['name'], entry['pwd'], entry['phone'])
            db.session.add(new_driver)
            db.session.commit()
            return True
        except:
            return False


def add_driver_to_event(driver_phone, event_id):
    """
    @purpose:
    @args: 
    @return:
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
    @purpose:
    @args: 
    @return:
    """ 
    driver = {"name": None, "phone": None}
    drivers = []
    for result in DD.query.filter_by(_driver_curr_event=event_id).all():
        driver['name'] = result._driver_name
        driver['number'] = result._driver_phone
        drivers.append(jsonify(driver))
    return drivers

