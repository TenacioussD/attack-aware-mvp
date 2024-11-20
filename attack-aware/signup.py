from flask import request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash  # Ensure password is hashed before storing it
from models import db, User
from datetime import datetime
from utils import convertBirthday


class Signup:
    def post(self):
        # Get data from signup form and assign them to instance variables
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        newPassword = request.form["newPassword"]
        birthday_str = request.form["birthday"]

        # Convert the birthday string to a date object
        birthday = convertBirthday(birthday_str, flash_category='signup') #call function from utils.py
        if not birthday:
            return redirect(url_for('home'))  # If conversion failed, redirect to the home page

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists.", 'signup')  # Specify which form the flash message should show up on ('signup')
            return redirect(url_for('home'))
        else:
            # Create a new user instance
            user = User(
                firstName=firstName,
                lastName=lastName,
                email=email,
                password=generate_password_hash(newPassword),  # Secure password storage
                birthday=birthday
            )
            # Add the new user to the database
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Please login.", 'signup')  # Specify which form the flash message should show up on ('signup')
            return redirect(url_for('home'))  # Redirect to home page after successful signup
