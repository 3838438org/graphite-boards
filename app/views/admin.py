__author__    = "Phil Hendren"
__copyright__ = "Copyright 2014, Mind Candy"
__credits__   = ["Phil Hendren"]
__license__   = "MIT"
__version__   = "1.0"

import hashlib
from flask import Blueprint, request, render_template, current_app, flash, abort
from flask_login import login_required, current_user
from app.modules.admin import update_password

admin  = Blueprint('admin', __name__)

@admin.route('/admin/profile')
@login_required
def profile():
    return render_template('pages/profile.html')


@admin.route('/admin/update/profile', methods=['POST'])
@login_required
def update_profile():
    id = request.form['id']
    if current_user.id == int(id):
        password = request.form['password']
        pwdhash = hashlib.md5(password+current_app.secret_key).hexdigest()
        update_password(id, pwdhash)
        flash('Password updated for %s' % current_user.username)
    else:
        abort(403)
    return render_template('pages/profile.html')
