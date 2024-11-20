from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Define the User class that maps to the 'User' table in the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    firstName = db.Column(db.String(20))  # First name, with a max length of 20 characters
    lastName = db.Column(db.String(30))  # Last name, with a max length of 30 characters
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email, must be unique and required
    password = db.Column(db.String, nullable=False)  # Password, required for every user
    birthday = db.Column(db.DateTime, nullable=True) 
    profilePic = db.Column(db.String(), nullable=True)  # Store the file path as a string
    is_admin = db.Column(db.Boolean, default=False)  # Mark if user is admin

    # Define how to represent a User object when printed or logged
    def __repr__(self):
        # Return a string that includes the email of the user in a readable format
        return f'<User {self.email}>'
        # For example, if the user's email is 'user@example.com', it will return '<User user@example.com>'

#allows system to compare user password with password stored in hash
    def set_password(self, password): 
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)