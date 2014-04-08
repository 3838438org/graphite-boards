import ldap
import hashlib
from flask import current_app, request, redirect, flash, url_for
from flask_login import login_user
from app import db
from app.models.login import User
from app.models.schema import Users
from app.modules.admin import create_user



def ldap_auth(username, password):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, current_app.config['LDAP_CERTIFICATE'])
    ldap_server = "ldaps://%s:636" %(current_app.config['LDAP_SERVER'])
    l = ldap.initialize(ldap_server)
    l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    bind_user = "uid=%s,%s,%s" %(username, current_app.config['LDAP_OU'], current_app.config['LDAP_BASEDN'])
    try:
        l.simple_bind_s(bind_user, password)
        return True
    except Exception, e:
        return False


def db_auth(username, password):
    user = Users.query.filter_by(username=username).first()
    pwdhash = hashlib.md5(password+current_app.secret_key).hexdigest()
    if user is not None:
        if pwdhash == user.password:
            return True
        else:
            user = False
    return user


def get_user(username, password):
    if not current_app.config['LDAP_ENABLED'] or username == 'admin':
        auth_user = db_auth(username, password)
        if auth_user:
            find_user = Users.query.filter_by(username=username).first()
        elif auth_user is None:
            create_user(username, password)
            find_user = Users.query.filter_by(username=username).first()
        else:
            find_user = None
    else:
        auth_user = ldap_auth(username, password)
        if auth_user:
            find_user = Users.query.filter_by(username=username).first()
            if find_user is None:
                create_user(username, password)
                find_user = Users.query.filter_by(username=username).first()

        else:
            find_user = None

    if find_user is not None:
        user = User(find_user.id, find_user.username, find_user.role)
    else:
        user = None
    return user



def do_login(get_user, auth_enabled=False):
    if not auth_enabled:
        testuser = Users.query.filter_by(username='TESTUSER').first()
        user = User(testuser.id, testuser.username)
    else:
        username = request.form["username"]
        password = request.form["password"]
        if username == 'TESTUSER':
            user = None
        else:
            user = get_user(username, password)
    
    if user is False:
        flash('Authentication failure')
        return redirect(url_for('dash.login'))
    
    if user:
        if login_user(user):
            return redirect(request.args.get("next") or url_for("dash.my_dashboards"))
        else:
            flash('Authentication failure')
            return redirect(url_for('dash.login'))
    else:
        flash('Authentication failure')
        return redirect(url_for('dash.login'))