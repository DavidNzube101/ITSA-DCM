from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user


import base64
import random
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


staff_actions = Blueprint('staff_actions', __name__)
sa = staff_actions

def getDBItem(model, column, value):
    
    try:
        i = dbORM.get_all(model)[f'{dbORM.find_one(model, column, value)}']
    except Exception as e:
        i = {}

    return i

@sa.route("/add-device", methods=['POST'])
def addDevice():
    numbers = []
    for x in range(10):
        numbers.append(x)

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uid = f'{random.choice(numbers)}{random.choice(numbers)}{random.choice(numbers)}{random.choice(numbers)}{random.choice(letters)}{random.choice(numbers)}{random.choice(numbers)}{random.choice(numbers)}{random.choice(letters)}'
    _ = {
        "name": request.form['Device_Name'], 
        "device_uid": uid, 
        "ip_address": "", 
        "mac_id": "", 
        "device_dob": request.form['Device_dob'],
        "category": request.form['Device_category'], 
        "last_maintained": request.form['Device_last_maintained'], 
        "connected_status": "Not Connected", 
        "device_health": "",
        "user_id": dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "email", request.form["user_email"])}']['id']
    }

    dbORM.add_entry("DeviceITSA", encrypt.encrypter(str(_)))
    if dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "email", request.form["user_email"])}']['privilege'] == 'staff':
        dvc = int(dbORM.get_all("StaffITSA")[f'{dbORM.find_one("StaffITSA", "email", request.form["user_email"])}']['device_count'])
        dbORM.update_entry("StaffITSA", dbORM.find_one("StaffITSA", "email", request.form['user_email']), encrypt.encrypter(str({"device_count": f"{dvc + 1}"})), False)

    
    return ScreenGoRoute.go_to("4")

@sa.route("/remove-device/<string:Device_id>")
def removeDevice(Device_id):

    try:
        dbORM.delete_entry("UserITSA", Device_id)
    except Exception as e:
        pass
    
    return ScreenGoRoute.go_to("4")

@sa.route("/connect-device/<string:did>")
def connectDevice(did):
    theDevice = dbORM.get_all("DeviceITSA")[f'{dbORM.find_one("DeviceITSA", "device_uid", did)}']
    u = dbORM.get_all("UserITSA")[current_user.id]
    
    return render_template("ConnectDevicePage.html", Device = theDevice, CUser = u, test_results = "Not Connected")

@sa.route("/test-connection/<string:did>", methods=['GET', 'POST'])
def test_connection(did):
    nc = "Not Connected"
    c = "Connected"
    o = "Offline"
    O = "Online"
    uid = did

    results = random.choice([o, O])

    dbORM.update_entry("DeviceITSA", dbORM.find_one("DeviceITSA", "device_uid", uid), encrypt.encrypter(str({"connected_status": results})), False)

    return ScreenGoRoute.go_to("4")

@sa.route("/request-maintainence", methods=['POST'])
def requestMaintenance():
    _ = {
        'description': request.form['description'], 
        'user_id': f"{current_user.id}", 
        'priority': request.form['request_priority'], 
        'section': request.form['request_section'], 
        'is_done': "false", 
        'device_id': request.form['device_uid'], 
        'org_id': f"{dbORM.get_all('UserITSA')[current_user.id]['organization_id']}"
    }
    dbORM.add_entry("RequestITSA", encrypt.encrypter(str(_)))
        
    return ScreenGoRoute.go_to("5")

@sa.route("/view-request/<string:req_id>")
def viewRequest(req_id):

    r = dbORM.get_all("RequestITSA")[f'{req_id}']
    
    return render_template("TheRequest.html", Request=r, CUser = dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "id", current_user.id)}'], GetDBItem = getDBItem)

@sa.route("/delete-request/<string:req_id>")
def deleteRequest(req_id):
    
    try:
        dbORM.delete_entry("RequestITSA", req_id)
    except Exception as e:
        pass

    return ScreenGoRoute.go_to("5")

@sa.route("/edit-request-priority", methods=['POST'])
def editRequestPriority():
    
    r = dbORM.get_all("RequestITSA")[f'{request.form["req_id"]}']

    dbORM.update_entry("RequestITSA", dbORM.find_one("RequestITSA", "id", request.form["req_id"]), encrypt.encrypter(str({"priority": f"{request.form['new_priority']}"})), False)

    
    return render_template("TheRequest.html", Request=r, CUser = dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "id", current_user.id)}'], GetDBItem = getDBItem)