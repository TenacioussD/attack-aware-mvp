from flask import request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash  # Ensure password is hashed before storing it
from models import db, User

class Signup:
    def post(self):
        # Get data from signup form and assign them to instance variables
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        newPassword = request.form["newPassword"]

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists.")
            return redirect(url_for('home'))
        else:
            # Create a new user instance
            user = User(
                firstName=firstName,
                lastName=lastName,
                email=email,
                password=generate_password_hash(newPassword)  # Secure password storage
            )
            # Add the new user to the database
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Please login.")
            return redirect(url_for('home'))  # Redirect to home page after successful signup