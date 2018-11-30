from flask import Flask, render_template, request, redirect, jsonify, url_for,flash
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Device as Device_db,Alarm
import alarm_check
import random
import string
import httplib2
import json
from flask import make_response
import requests
from jnpr.junos import Device
import time
from netmiko import ConnectHandler

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///alarmsAndDevices.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

devices=session.query(Device_db).all()

active_alarms = []

@app.route('/')
@app.route('/tool/')
def displayAlarm():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    latest_alarms = []
    alarms = session.query(Alarm).order_by((Alarm.id.desc()))
    for alarm in alarms:
        latest_alarms.append([alarm.detail,alarm.id,session.query(Device_db)
                            .filter_by(ip=alarm.device_ip).one().name,alarm.alarm_time])
        if len(latest_alarms) >= 10:
            break
    return render_template('ALARMS.html', latest_alarms=latest_alarms)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

