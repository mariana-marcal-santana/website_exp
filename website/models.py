# storing databases models
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now()) # default=db.func.now() means that the date will be the current date
    # creating a relationship between the user and the notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # when creating a new note, a valid user.id must be provided

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # unique=True means that the email must be unique
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    # creating a relationship between the user and the notes
    notes = db.relationship('Note')
