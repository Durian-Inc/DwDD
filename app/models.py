from flask_sqlalchemy import SQLAlchemy

from app import app

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/debate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class DesignatedDriver(db.Model):
    """Account for each registered driver
    Attributes:
        _driver_name: The full name of the driver
        _driver_password: The driver's password
        _driver_phone: The driver's phone number
    """
    __tablename__ = "drivers"

    _driver_name = db.Column(db.String, nullable=False)
    _driver_password = db.Column(db.String, nullable=False)
    _driver_phone = db.Column(db.String, nullable=False, unique=True, primary_key=True)

    def __init__(self, name, password, phone_number):
        self._driver_name = name
        self._driver_password = password
        self._driver_phone = phone_number

    def __repr__(self):
        return '<Driver %r>' % (self._driver_name)


class Event(db.Model):
    """Account for each event
    Attributes:
        _name: The name of the event
        _start_time: The start time of the event
        _end_time: The end time of the event
    """
    __tablename__ = "events"

    _name = db.Column(db.String, nullable=False, primary_key=True)
    _start_time = db.Column(db.String, nullable=False, primary_key=True)
    _end_time = db.Column(db.String, nullable=False, primary_key=True)

    def __init__(self, name, start, end):
        self._name = name
        self._start_time = start
        self._end_time = end

    def __repr__(self):
        return '<Event %r>' % (self._name)
