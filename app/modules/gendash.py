__author__    = "Phil Hendren"
__copyright__ = "Copyright 2014, Mind Candy"
__credits__   = ["Phil Hendren"]
__license__   = "MIT"
__version__   = "1.0"

from app import db
import json
import cPickle

from app.models.schema import Dashboard, Graph, Users


def get_all_dashboards():
    return Dashboard.query.all()


def get_dashboard(id):
    return Dashboard.query.filter_by(id=id).first()

def get_all_dashboards_for_user(username):
    return Dashboard.query.filter_by(owner=username).all()


def get_dashboard_for_user(username):
    return Dashboard.query.filter_by(owner=username).first()


def create_dashboard(dashboard, owner):
    new = Dashboard(dashboard, owner)
    new.layout = cPickle.dumps({})
    db.session.add(new)
    db.session.commit()
    return True


def delete_dashboard(id):
    d = get_dashboard(id)
    db.session.delete(d)
    db.session.commit()
    urls = Graph.query.all()
    for record in urls:
        if record.dashboard_id is None:
            db.session.delete(record)
    db.session.commit()
    return True


def get_url(id):
    return Graph.query.filter_by(id=id).first()


def add_url(url, name, id):
    d = get_dashboard(id)
    g = Graph(url, name, d)
    db.session.add(g)
    db.session.commit()
    return True


def delete_url(id):
    u = get_url(id)
    db.session.delete(u)
    db.session.commit()
    return True


def update_graph(id, name, url):
    update = get_url(id)
    update.url = url
    update.name = name
    db.session.commit()
    return True

def update_layout(json_obj):
    layout = json_obj[json_obj.keys()[0]]

    # JSON doesn't support integer keys. Grumble grumble.
    layout = dict(map(lambda (key, value): (int(key), value), layout.items()))
    pickled = cPickle.dumps(layout)

    dashboard = get_dashboard(json_obj.keys()[0])
    dashboard.layout = pickled
    db.session.commit()
    return pickled



