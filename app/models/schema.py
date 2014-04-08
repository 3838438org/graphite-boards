from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    role     = db.Column(db.Integer)

    def __init__(self, username, password=None, role=2):
        self.username = username
        self.password = password
        self.role     = role


class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    name = db.Column(db.Text)


    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'))
    dashboard = db.relationship('Dashboard',
        backref=db.backref('graphes', lazy='dynamic'))

    def __init__(self, url, name, dashboard):
        self.url = url
        self.name = name
        self.dashboard = dashboard

    def __repr__(self):
        return '<Graph %r>' % self.url


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    owner = db.Column(db.String(100))
    layout = db.Column(db.Text)

    def __init__(self, name, owner, layout=None):
        self.name = name
        self.owner = owner
        self.layout = layout

    def __repr__(self):
        return '<Dashboard %r>' % self.name
