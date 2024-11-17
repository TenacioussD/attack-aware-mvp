from flask import request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash  # Ensure password is hashed before storing it
from models import db, User
from datetime import datetime


class Signup:
    def post(self):
        # Get data from signup form and assign them to instance variables
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        newPassword = request.form["newPassword"]
        birthday_str = request.form["birthday"]

        # Convert the birthday string to a date object
        try:
          birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        except ValueError:
          flash("Invalid birthday format. Please use YYYY-MM-DD", 'signup')
          return redirect(url_for('home'))


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
