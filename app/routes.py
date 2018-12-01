import os

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from twilio.rest import Client
from twilio.twiml.voice_response import Say, VoiceResponse

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return render_template('listview.html')


@app.route('/a', methods=['GET', 'POST'])
def bonk():
    if request.method == 'GET':
        return render_template('drunkview.html')
    elif request.method == 'POST':
        # nums = ['+13145876003', '+13146517436']
        nums = ['+13145876003']
        for num in nums:
            call(num)
        return redirect('/sos', code=302)


@app.route('/sos', methods=['GET'])
def sos():
    return render_template('sos.html')


@app.route('/d')
def bink():
    return render_template('ddview.html')


@app.route('/login')
def log():
    return render_template('login.html')


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

    print(call.sid)
