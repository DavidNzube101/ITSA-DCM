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


super_admin_actions = Blueprint('super_admin_actions', __name__)
saa = super_admin_actions

@saa.route('/onboard-organization', methods=['POST'])
def onboardOrganization():

    _ = {
        "name" : f"{request.form['Organization_Name']}",
        "sector" : f"{request.form['Organization_Sector']}",
        "password": "",
        "staff_count" : f"{request.form['Organization_Staff_Count']}",
        "email" : f"{request.form['Organization_Email']}",
        "location" : f"{request.form['Organization_Location']}",
        "phone_number" : f"{request.form['Organization_Phone_Number']}",
        "website" : f"{request.form['Organization_Website']}",
        "socials1" : f"{request.form['Organization_Socials_1']}",
        "socials2" : f"{request.form['Organization_Socials_2']}"
    }

    dbORM.add_entry("OrganizationITSA", f"{encrypt.encrypter(str(_))}")
    
    return ScreenGoRoute.go_to("3")

@saa.route("/view-organization/<string:organization_id>")
def viewOrganization(organization_id):

    a = dbORM.get_all("OrganizationITSA")[f'{organization_id}']
    
    return render_template("TheOrganization.html", org=a)

@saa.route("/remove-organization/<string:organization_id>")
def removeOrganization(organization_id):

    dbORM.delete_entry("OrganizationITSA", organization_id)
    
    return ScreenGoRoute.go_to("3")

@saa.route('/onboard-technician', methods=['POST'])
def onboardTechnician():

    _ = {
        "name" : f"{request.form['Technician_Name']}",
        "skill_set" : f"{request.form['Technician_Skillset']}",
        "yop" : f"{request.form['Technician_Years_of_Proficiency']}",
        "email" : f"{request.form['Technician_Email']}",
        "location" : f"{request.form['Technician_Location']}",
        "phone_number" : f"{request.form['Technician_Phone_Number']}"
    }

    dbORM.add_entry("TechnicianITSA", f"{encrypt.encrypter(str(_))}")
    
    return ScreenGoRoute.go_to("2")

@saa.route("/view-technician/<string:Technician_id>")
def viewTechnician(Technician_id):

    t = dbORM.get_all("TechnicianITSA")[f'{Technician_id}']
    
    return render_template("TheTechnician.html", tch=t)

@saa.route("/remove-technician/<string:Technician_id>")
def removeTechnician(Technician_id):

    dbORM.delete_entry("TechnicianITSA", Technician_id)
    
    return ScreenGoRoute.go_to("2")