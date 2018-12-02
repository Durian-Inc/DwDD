from flask_sqlalchemy import SQLAlchemy

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost:5432/DWDD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class DesignatedDriver(db.Model):
    """Account for each registered driver
    Attributes:
        _driver_name: The full name of the driver
        _driver_password: The driver's password
        _driver_phone: The driver's phone number
        _driver_curr_event: The event that they currently are DDing
    """
    __tablename__ = "designateddriver"

    _driver_name = db.Column(db.String, nullable=False)
    _driver_password = db.Column(db.String, nullable=False)
    _driver_phone = db.Column(
        db.String, nullable=False, unique=True, primary_key=True)
    _driver_curr_event = db.Column(db.Integer, nullable=True)
    _driver_is_available = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, password, phone_number):
        self._driver_name = name
        self._driver_password = password
        self._driver_phone = phone_number
        self._driver_is_available = True

    def __repr__(self):
        return '<Driver %r>' % (self._driver_name)


class Event(db.Model):
    """Account for each event
    Attributes:
        _name: The name of the event
        _start_time: The start time of the event
        _end_time: The end time of the event
        _event_id: 
    """
    __tablename__ = "events"

    _name = db.Column(db.String, nullable=False)
    _start_time = db.Column(db.String, nullable=False)
    _end_time = db.Column(db.String, nullable=False)
    _event_id = db.Column(
        db.Integer, nullable=False, unique=True, primary_key=True)

    def __init__(self, name, start, end, event_id):
        self._name = name
        self._start_time = start
        self._end_time = end
        self._event_id = event_id

    def __repr__(self):
        return '<Event %r>' % (self._name)
