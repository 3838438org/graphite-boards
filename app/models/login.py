from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, role, active=True):
        self.id = id
        self.username = username
        self.role = role
        self.active = active

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True  

    def is_anonymous(self):
        return False

    def user_id(self):
        return self.id

    def username(self):
        return self.username

    def role(self):
        return self.role

