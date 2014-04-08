__author__    = "Phil Hendren"
__copyright__ = "Copyright 2014, Mind Candy"
__credits__   = ["Phil Hendren"]
__license__   = "MIT"
__version__   = "1.0"

import os
import ldap
import hashlib
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


#------------------------------
# Initialise the Flask app
#------------------------------
app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s' % app.config['DB_PATH']
app.secret_key = 'sdfgsd56476yrthgkvfcx' # you should change this to something equally random
db = SQLAlchemy(app)


#-------------------------------
# Import our Models
#-------------------------------
from app.models.schema import Users, Graph, Dashboard
from app.models.login import User

#-------------------------------
# Import helpers
#-------------------------------
from app.modules.auth import ldap_auth, db_auth
from app.modules.admin import create_user


#---------------------------------
# Create the sqlite db
#---------------------------------
@app.before_first_request
def create_db():
    if not os.path.exists(app.config['DB_PATH']):
        db.create_all()
        TESTUSER = Users(username='TESTUSER')
        pwdhash  = hashlib.md5('admin'+app.secret_key).hexdigest()
        ADMIN    = Users(username='admin', password=pwdhash, role=1)
        db.session.add(TESTUSER)
        db.session.add(ADMIN)
        db.session.commit()


#---------------------------------
# Custom error handlers
#---------------------------------
@app.errorhandler(404)
def forbidden(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internalerror(e):
    return render_template('errors/500.html'), 500


#------------------------------
# Initalise the login manager
#------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.unauthorized_handler
def unauthorized():
    return render_template('pages/login.html')


@login_manager.user_loader
def load_user(id):
    if not app.config['AUTH_ENABLED']:
        user = Users.query.filter_by(id=id).first()
    else:
        user = Users.query.filter_by(id=id).first()
    return User(user.id, user.username, user.role)


#-------------------------------
# Import our Blueprints
#-------------------------------
from views.main import dash as dash
from views.admin import admin as admin
app.register_blueprint(dash)
app.register_blueprint(admin)