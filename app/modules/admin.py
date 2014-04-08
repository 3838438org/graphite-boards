import hashlib
from flask import current_app
from app import db
from app.models.schema import Users


def create_user(username, password):
    pwdhash = hashlib.md5(password+current_app.secret_key).hexdigest()
    new_user = Users(username=username, password=pwdhash)
    db.session.add(new_user)
    db.session.commit()


def update_password(id, password):
    user = Users.query.filter_by(id=id).first()
    user.password = password
    db.session.commit()
    return True
