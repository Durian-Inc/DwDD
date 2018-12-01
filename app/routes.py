import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import DesignatedDriver

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def AddUser(name, phone, pwd):
    try:
        new_driver = DesignatedDriver(name, phone, pwd)
        db.session.add(new_driver)
        db.session.commit()
        return True
    except:
        return False


def GetUserFromDB():
    drivers = DesignatedDriver.query.all()
    names = []
    for driver in drivers:
        names.append(driver._name)
    return names

@app.route('/')
def hello():
    print("Adding user")
    AddUser("Tom Ford", "3146517436", "pass@word1")
    print("Added user")
    names = GetUserFromDB()
    print(names)
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)
