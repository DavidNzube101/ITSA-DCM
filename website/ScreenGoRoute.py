from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from .db import dbORM
from . import DateToolKit as dtk

import base64
import imghdr
from . import encrypt
import random
import datetime as dt
from datetime import datetime

def getOppositeTheme(theme):
	if theme == 'light':
		return 'dark'
	else:
		return 'light'

def getDateTime():
	# Getting Date-Time Info
	current_date = dt.date.today()
	current_time = datetime.now().strftime("%H:%M:%S")

	# Date Format: "YYYY-MM-DD"
	formatted_date = current_date.strftime("%Y-%m-%d")
	date = formatted_date
	time = current_time

	return [date, time]

def HTMLBreak(n):
	breaks = ""

	for x in range(int(n)):
		breaks = breaks + "\n<br>"	

	return breaks

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else 'application/pdf'

def calcTimeDifference(dpt, ct):
	return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]

def toJoin(i, j):
	return f"{i}{j}"

User, Record = dbORM.get_all("UserITSA"), None

def getAppThemeData():
	AppTheme = dbORM.get_all("UserITSA")[f'{current_user.id}']['user_theme'],
	AppThemeOpposite = getOppositeTheme(dbORM.get_all("UserITSA")[f'{current_user.id}']['user_theme']),


	dark_app_theme = {
		"Main Background": "#0c1d2f",
		"Main Text": "antiquewhite",
		"Button Background": "purple",
		"Button Text": "white"
	}

	light_app_theme = {
		"Main Background": "ghostwhite",
		"Main Text": "black",
		"Button Background": "mediumpurple",
		"Button Text": "white"
	}

	# print(type(AppTheme))

	if AppTheme[0] == "light":
		app_theme = light_app_theme
	else:
		app_theme = dark_app_theme

	return app_theme

def getAdminCount(organization_id):
	
	return organization_id

def getDeviceStatus(device_uid):
	if dbORM.get_all("DeviceITSA")[f'{dbORM.find_one("DeviceITSA", "device_uid", device_uid)}']['connected_status'] == "Not Connected":
		return "Not Connected"
	else:
		dummy_server = {
			"1": ["true", {}],
			"2": ["false", None],
			"box": ['1', '2']
		}
		listen = random.choice([dummy_server['1'], dummy_server['2']])
		if listen[0] == "true":
			data = listen[1]
			dbORM.update_entry("DeviceITSA", dbORM.find_one("DeviceITSA", "device_uid", device_uid), encrypt.encrypter(str({"connected_status": "Online"})), False)
			return "Online"
		else:
			dbORM.update_entry("DeviceITSA", dbORM.find_one("DeviceITSA", "device_uid", device_uid), encrypt.encrypter(str({"connected_status": "Offline"})), False)
			return "Offline"

def getStaffInfo(staff_id):
	s = dbORM.get_all("StaffITSA")[f'{dbORM.find_one("StaffITSA", "id", staff_id)}']
	return {"device_count": s['device_count'], "email": s['email']}
	
def getDBItem(model, column, value):
	
	try:
		i = dbORM.get_all(model)[f'{dbORM.find_one(model, column, value)}']
	except Exception as e:
		i = {}

	return i

def go_to(screen_id, _redirect=False, **kwargs):
	if _redirect == False:
		u = dbORM.get_all("UserITSA")[f'{current_user.id}']
		Organizations = dbORM.get_all("OrganizationITSA")
		Organizations_list = []
		for k, v in Organizations.items():
			Organizations_list.append(v)

		Technicians = dbORM.get_all("TechnicianITSA")
		Technicians_list = []
		for k, v in Technicians.items():
			Technicians_list.append(v)

		Devices = dbORM.get_all("DeviceITSA")
		Devices_list = []
		for k, v in Devices.items():
			Devices_list.append(v) #"0": {"id": "0", "name": "NULL", "device_uid": "NULL", "ip_address": "NULL", "mac_id": "NULL", "category": "NULL", "last_maintained": "NULL", "connected_status": "NULL", "device_health": "NULL"}
		# Requests = dbORM.get_all("RequestITSA")
		# Requests_list = []
		# for k, v in Requests.items():
		# 	Requests_list.append(v)
		Requests_list = dbORM.find_all("RequestITSA", "org_id", u['organization_id'])

		Staffs = dbORM.get_all("StaffITSA")
		Staffs_list = []
		for k, v in Staffs.items():
			Staffs_list.append(v)

		# print(Staffs_list)

		def theORG():
			if u['organization'] == "":
				return "None"
			else:
				return dbORM.get_all("OrganizationITSA")[f'{dbORM.find_one("OrganizationITSA", "id", u["organization_id"])}']

		try:
			r = dbORM.find_all("RequestITSA", "user_id", current_user.id)
			d = dbORM.find_all("DeviceITSA", "user_id", current_user.id)
			# print(r, d)
		except Exception as e:
			r = "None"
			d = "None"
			
	
		return render_template("dashboard.html",
			CUser = u,
			Organizations = Organizations_list,
			the_Organization = theORG(),
			Technicians = Technicians_list,
			Devices = Devices_list,
			MyDevices = d,
			ARequests = Requests_list,
			Staffs = Staffs_list,
			MyRequests = r,

			ScreenID = screen_id,

			AppTheme = getAppThemeData(),

			DTK = dtk,
			LengthFunc = len,
			ToJoin = toJoin,
			GetAdminCount = getAdminCount,
			GetDBItem = getDBItem,
			GetStaffInfo = getStaffInfo,
			GetDeviceStatus = getDeviceStatus,
			ToString = str,
			getMIME = get_mime_type,
			TimeDifference = calcTimeDifference,
			CurrentTime = getDateTime()[1],
			HTMLBreak_ = HTMLBreak
		)
	else:
		return redirect(url_for("views.dashboard"))
	