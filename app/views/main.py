__author__    = "Phil Hendren"
__copyright__ = "Copyright 2014, Mind Candy"
__credits__   = ["Phil Hendren"]
__license__   = "MIT"
__version__   = "1.0"

import hashlib
import json
import cPickle
import sys
from flask import Blueprint, request, render_template, redirect, url_for, current_app, flash, abort
from flask_login import login_required, logout_user, current_user
from app.modules.auth import do_login, get_user
from app.modules.admin import update_password
from app.settings import AUTH_ENABLED
import app.modules.gendash as gendash


dash  = Blueprint('dash', __name__)


@dash.route("/login", methods=["GET", "POST"])
def login():
    if not AUTH_ENABLED:
        return do_login(get_user)
    if request.method == 'POST':
        return do_login(get_user, auth_enabled=True)
    elif current_user.is_authenticated():
        return redirect(url_for('dash.index'))
    else:
        return render_template('pages/login.html')


@dash.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@dash.route('/')
def index():
    dashboards = gendash.get_all_dashboards()
    return render_template('pages/dash.html', dashboards=dashboards, auth_enabled=AUTH_ENABLED)


@dash.route('/dashboard/<id>')
def dashboard(id):
    dashboard = gendash.get_dashboard(id)
    if dashboard is None:
        abort(404)
    try:
        dashboard.layout = cPickle.loads(dashboard.layout.encode('utf-8'))
    except: 
        print "Unexpected error:", sys.exc_info()[0]
        raise
    return render_template('pages/dashboard.html', dashboard=dashboard)


@dash.route('/mydashboards')
@login_required
def my_dashboards():
    dashboards = gendash.get_all_dashboards_for_user(current_user.username)
    return render_template('pages/mydashboards.html', dashboards=dashboards)


@dash.route('/create/dashboard', methods=['POST'])
@login_required
def create_dashboard():
    gendash.create_dashboard(request.form['dashboard'], request.form['username'])
    return redirect(url_for('dash.my_dashboards'))


@dash.route('/delete/dashboard/<id>')
@login_required
def delete_dashboard(id):
    dashboard = gendash.get_dashboard(id)
    if dashboard.owner == current_user.username or current_user.role == 1:
        gendash.delete_dashboard(id)
    return redirect(url_for('dash.my_dashboards'))


@dash.route('/edit/dashboard/<id>')
@login_required
def edit_dashboard(id):
    dashboard = gendash.get_dashboard(id)
    if dashboard.owner == current_user.username or current_user.role == 1:
        dashboard = gendash.get_dashboard(id)
        return render_template('pages/edit.html', dashboard=dashboard)
    else:
        return redirect(url_for('dash.my_dashboards'))


@dash.route('/add/url', methods=['POST'])
@login_required
def add_url():
    dashboard = gendash.get_dashboard(request.form['dashboard'])
    if dashboard.owner == current_user.username or current_user.role == 1:
        gendash.add_url(request.form['url'], request.form['name'], 
                        request.form['dashboard'])
        return redirect('/edit/dashboard/%s' % request.form['dashboard'])
    else:
        return redirect(url_for('dash.my_dashboards'))


@dash.route('/delete/graph/<dashboard_id>/<graph_id>')
@login_required
def delete_url(dashboard_id, graph_id):
    dashboard = gendash.get_dashboard(dashboard_id)
    if dashboard.owner == current_user.username or current_user.role == 1:
        gendash.delete_url(graph_id)
        return redirect('/edit/dashboard/%s' % dashboard_id)
    else:
        return redirect(url_for('dash.my_dashboards'))


@dash.route('/edit/graph', methods=['POST'])
@login_required
def edit_url():
    dashboard_id = request.form['dashboard_id']
    graph_id     = request.form['graph_id']
    graph_name   = request.form['graph_name']
    graph_url    = request.form['graph_url']
    dashboard = gendash.get_dashboard(dashboard_id)
    if dashboard.owner == current_user.username or current_user.role == 1:
        gendash.update_graph(graph_id, graph_name, graph_url)
        return redirect('/edit/dashboard/%s' % dashboard_id)
    else:
        return redirect(url_for('dash.my_dashboards'))


@dash.route('/update/layout', methods=['PUT'])
def update_layout():
    payload = request.get_json()
    pickled = gendash.update_layout(payload)
    return pickled






