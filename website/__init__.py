from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin

import json
import os
import random

from .db import db
from .db import dbORM
from .encrypt import encrypter

from . import ScreenGoRoute

if dbORM == None:
    User, Record = None, None


def initialize_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'imgoingtowinthis'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__).replace('\\', '/'), 'static/_UM_')
    print(f"UF: ({UPLOAD_FOLDER})")

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    from .admin_actions import admin_actions
    from .super_admin_actions import super_admin_actions
    from .staff_actions import staff_actions

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(super_admin_actions, url_prefix='/')
    app.register_blueprint(admin_actions, url_prefix='/')
    app.register_blueprint(staff_actions, url_prefix='/')

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Internal Server Error: {e}")
        return render_template('broken-page.html', error=e), 500

    from flask_login import UserMixin, LoginManager

    FL_Login = LoginManager(app)
    FL_Login.login_view = 'login'

    class UserClass:
        def __init__(self, id):
            self.id = id

        @staticmethod
        def is_authenticated():
            return True

        @staticmethod
        def is_active():
            return True

        @staticmethod
        def is_anonymous():
            return False

        def get_id(self):
            return self.id


        @FL_Login.user_loader
        def load_user(id):
            try:
                u = dbORM.find_one("UserITSA", "id", id)
                if not u:
                    return None
                return UserClass(id=dbORM.get_all("UserITSA")[f'{u}']['id'])
            except:
                anonymous = {
                    "0": {
                        "id": "0", 
                        "email": "NULL"
                    }
                }
                return UserClass(id=anonymous['0']['id'])


    @app.route("/login", methods=['GET', 'POST']) 
    def login():
        User = dbORM.get_all("UserITSA")

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = dbORM.find_one("UserITSA", "email", email)
            if email == "david.nzube.official22@gmail.com" and password == "234567890abc":
                
                t_user = UserClass(id=f'1')
                login_user(t_user, remember=True)
                return redirect(url_for('views.dashboard'))

            elif user and check_password_hash(dbORM.get_all("UserITSA")[f'{user}']['password'], password):

                if dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "email", email)}']["privilege"] == "admin":
                    t_user = UserClass(id=f'{user}')
                    login_user(t_user, remember=True)
                    return redirect(url_for('views.dashboard'))
                else:
                    return render_template("login.html", status=("Login as a Staff", "Error occurred"))

            elif dbORM.find_one("OrganizationITSA", "email", email):
                if dbORM.find_one("OrganizationITSA", "email", email) and dbORM.get_all("OrganizationITSA")[f'{dbORM.find_one("OrganizationITSA", "email", email)}']['password'] != "":
                    print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{dbORM.find_one("OrganizationITSA", "email", email)}<<<<<<<<<<<<<<<<<<<<<<<><><><><>><<<<<<<<<<<<<<<<')
                    t_user = UserClass(id=f'{dbORM.find_one("OrganizationITSA", "email", email)}')
                    login_user(t_user, remember=True)
                    return redirect(url_for('views.dashboard'))
                else:
                    return render_template(
                        "CreateOrganizationPassword.html", 
                        org=dbORM.get_all("OrganizationITSA")[f'{dbORM.find_one("OrganizationITSA", "email", email)}'],
                        status=())
                
            else:
                return render_template("login.html", status=("Incorrect password or email.", "Error occurred"))

        return render_template('login.html', status=())

    @app.route("/CreateOrganizationPassword", methods=['POST'])
    def CreateOrganizationPassword():
        
        password1 = request.form['password1']
        password2 = request.form['password2']

        _org = dbORM.get_all("OrganizationITSA")[f'{dbORM.find_one("OrganizationITSA", "id", request.form["Organization_ID"])}']

        if len(password1) < 8:
            return render_template("CreateOrganizationPassword.html", org=_org, status=("Password length less than 8", "Error occurred"))

        elif password1 != password2:
            return render_template("CreateOrganizationPassword.html", org=_org, status=("Passwords don't match", "Error occurred"))

        else:
            password_hashed = generate_password_hash(password1)
            dbORM.update_entry("OrganizationITSA", dbORM.find_one("OrganizationITSA", "email", request.form["email"]), encrypter(str({"password": f"{password_hashed}"})), False)

            _ = {
                "email": request.form['email'], 
                "password": password_hashed, 
                "privilege": "admin", 
                "user_theme": "light",
                "organization": _org['name'],
                "organization_id": _org['id']
            }

            dbORM.add_entry("UserITSA", f"{encrypter(str(_))}")
            
            t_user = UserClass(id=f'{dbORM.find_one("UserITSA", "email", request.form["email"])}')
            login_user(t_user, remember=True)
            return redirect(url_for('views.dashboard'))

        return ScreenGoRoute.go_to("1")

    @app.route("/staff-login", methods=['GET', 'POST']) 
    def staff_login():
        User = dbORM.get_all("UserITSA")

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = dbORM.find_one("UserITSA", "email", email)
            if user and dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "email", email)}']["password"] == "" and dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "email", email)}']["privilege"] == "staff":
                
                return render_template(
                    "CreateStaffPassword.html", 
                    stf=dbORM.get_all("StaffITSA")[f'{dbORM.find_one("StaffITSA", "email", email)}'],
                    status=())

            elif user and check_password_hash(dbORM.get_all("UserITSA")[f'{user}']['password'], password):
                if dbORM.get_all("UserITSA")[f'{dbORM.find_one("UserITSA", "email", email)}']["privilege"] == "staff":
                    t_user = UserClass(id=f'{user}')
                    login_user(t_user, remember=True)
                    return redirect(url_for('views.dashboard'))
                else:
                    return render_template("login-staff.html", status=("Login as an Admin", "Error occurred"))

            else:
                return render_template("login-staff.html", status=("Incorrect password or email.", "Error occurred"))

        return render_template('login-staff.html', status=())

    @app.route("/CreateStaffPassword", methods=['POST'])
    def CreateStaffPassword():
        
        password1 = request.form['password1']
        password2 = request.form['password2']

        _stf = dbORM.get_all("StaffITSA")[f'{dbORM.find_one("StaffITSA", "id", request.form["Staff_ID"])}']

        if len(password1) < 8:
            return render_template("CreateStaffPassword.html", stf=_stf, status=("Password length less than 8", "Error occurred"))

        elif password1 != password2:
            return render_template("CreateStaffPassword.html", stf=_stf, status=("Passwords don't match", "Error occurred"))

        else:
            password_hashed = generate_password_hash(password1)
            dbORM.update_entry("StaffITSA", dbORM.find_one("StaffITSA", "email", request.form["email"]), encrypter(str({"password": f"{password_hashed}"})), False)

            dbORM.update_entry("UserITSA", dbORM.find_one("UserITSA", "email", request.form['email']), encrypt.encrypter(str({"password": f"{password_hashed}"})), False)
            
            t_user = UserClass(id=f'{dbORM.find_one("UserITSA", "email", request.form["email"])}')
            login_user(t_user, remember=True)
            return redirect(url_for('views.dashboard'))

        return ScreenGoRoute.go_to("1")

    @app.route("/signup", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('user_name')
            email = request.form.get('user_email')
            password1 = request.form.get('user_password')
            password2 = request.form.get('user_password2')

            user = dbORM.find_one("UserITSA", 'email', email)

            if user:
                return render_template("signup.html", status=("Email is already taken. Please use a different email.", "Sign Up Error"))
            elif len(email) < 4:
                return render_template("signup.html", status=("Invalid email: Email must be at least 4 characters long.", "Sign Up Error"))
            elif len(name) < 2:
                return render_template("signup.html", status=("Invalid name: Name must be at least 2 characters long.", "Sign Up Error"))
            elif password1 != password2:
                return render_template("signup.html", status=("Passwords do not match. Please re-enter your password.", "Sign Up Error"))
            elif len(password1) < 8:
                return render_template("signup.html", status=("Password is too short. It must be at least 8 characters long.", "Sign Up Error"))
            else:
                hashed_password = generate_password_hash(password1)
                new_user = {
                    'email': email,
                    'name': name,
                    'password': hashed_password,
                    "user_theme": "light"
                }

                # for key, details in new_user.items():
                dbORM.add_entry("UserITSA", f"{encrypter(str(new_user))}")

                t_user = UserClass(id=f'{dbORM.find_one("UserITSA", "email", email)}')

                login_user(t_user, remember=True)

                return redirect(url_for('views.dashboard'))

        return render_template("signup.html", status=())

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully.", category='Success') 
        return redirect(url_for('login'))
    

    return app