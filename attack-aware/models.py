from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Define the User class that maps to the 'User' table in the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    firstName = db.Column(db.String(20))  # First name, with a max length of 20 characters
    lastName = db.Column(db.String(30))  # Last name, with a max length of 30 characters
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email, must be unique and required
    password = db.Column(db.String, nullable=False)  # Password, required for every user
