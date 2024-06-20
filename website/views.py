from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user


import base64
import imghdr
import datetime as dt

from . import DateToolKit as dtk
from .db import db
from .db import dbORM
from . import encrypt
from . import ScreenGoRoute

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("UserITSA"), None


today = dt.datetime.now().date()


views = Blueprint('views', __name__)

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else ''

def getDBItem(model, column, value):
    
    try:
        i = dbORM.get_all(model)[f'{dbORM.find_one(model, column, value)}']
    except Exception as e:
        i = {}

    return i

@views.route("/")
def welcome():
    
    return render_template("landing.html")

@views.route("/dashboard")
@login_required
def dashboard():
    
    return ScreenGoRoute.go_to("1")

@views.route("/dashboard/<string:screen_number>")
@login_required
def dashboardPages(screen_number):
    
    return ScreenGoRoute.go_to(screen_number)

@views.route("/device/<string:uid>")
def viewDevice(uid):
    u = dbORM.get_all("UserITSA")[current_user.id]
    theDevice = dbORM.get_all("DeviceITSA")[f'{dbORM.find_one("DeviceITSA", "device_uid", uid)}']
    r = dbORM.find_all("RequestITSA", "device_id", theDevice['device_uid'])
    
    return render_template("ViewDevicePage.html", CUser = u, Device = theDevice, Requests = r, GetDBItem = getDBItem)