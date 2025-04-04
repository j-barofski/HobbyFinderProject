from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # database

class User(db.Model): # user class
    _tablename__ = 'users' # connect to the users table
    user_id = db.Column(db.Integer, primary_key=True) 
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    hobbies = db.relationship('Hobby', secondary='user_hobbies', backref='users') # create a relationship with users and hobbies


class Hobby(db.Model): # hobby class
    __tablename__ = 'hobbies' # connect to the hobbies table
    hobby_id = db.Column(db.Integer, primary_key=True)
    hobby_name = db.Column(db.String(100))

class UserHobby(db.Model): # User hobbies class - the relationship between the users and hobbies
    __tablename__ = 'user_hobbies' # connect to the user_hobbies table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobbies.hobby_id'), primary_key=True)