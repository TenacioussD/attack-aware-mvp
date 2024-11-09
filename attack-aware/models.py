from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20)) #first name can take 20 characters
    lastName = db.Column(db.String(30)) #Last name can take 30 characters
    email = db.Column(db.String(100), unique=True, nullable=False) #email can be a string of 100 characters, has to be unique and a user can not exsits without one
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'