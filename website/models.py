from . import db
from flask_login import UserMixin

class SavedRoute(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   routeName = db.Column(db.String(150), unique=True)
   summary = db.Column(db.String(150))
   origin = db.Column(db.String(150))
   originRaw = db.Column(db.String(150))
   destination = db.Column(db.String(150))
   destinationRaw = db.Column(db.String(150))
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    routes = db.relationship('SavedRoute')