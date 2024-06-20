from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user


import base64
import imghdr
import random
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


admin_actions = Blueprint('admin_actions', __name__)
aa = admin_actions

@aa.route('/onboard-staff', methods=['POST'])
def onboardStaff():
    u = dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "id", current_user.id)}']
    _org = dbORM.get_all("OrganizationITSA")[f'{dbORM.find_one("OrganizationITSA", "id", u["organization_id"])}']

    _ = {
        "email": request.form['Staff_Email'], 
        "password": "", 
        "privilege": "staff", 
        "user_theme": "light",
        "organization": _org['name'],
        "organization_id": _org['id']
    }
    dbORM.add_entry("UserITSA", f"{encrypt.encrypter(str(_))}")

    _s = {
        "name" : f"{request.form['Staff_Name']}",
        "job_title" : f"{request.form['Staff_job_title']}",
        "department" : f"{request.form['Staff_department']}",
        "working_hours" : f"{request.form['Staff_working_hours']}",
        "device_count" : f"0",
        "user_id": f"{dbORM.find_one('UserITSA', 'email', request.form['Staff_Email'])}",
        "location" : f"{request.form['Staff_Location']}",
        "phone_number" : f"{request.form['Staff_Phone_Number']}",
        "email": request.form['Staff_Email']
    }

    dbORM.add_entry("StaffITSA", f"{encrypt.encrypter(str(_s))}")
    # print(_, _s)
    return ScreenGoRoute.go_to("6")

@aa.route("/view-staff/<string:Staff_id>")
def viewStaff(Staff_id):

    t = dbORM.get_all("UserITSA")[f'{Staff_id}']
    
    return render_template("TheStaff.html", stf=t)

@aa.route("/remove-staff/<string:Staff_id>/<string:Staff_email>")
def removeStaff(Staff_id, Staff_email):

    try:
        dbORM.delete_entry("StaffITSA", Staff_id)
        dbORM.delete_entry("UserITSA", Staff_email)
    except Exception as e:
        pass
    
    return ScreenGoRoute.go_to("6")