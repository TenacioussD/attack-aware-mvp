from flask import request, flash, redirect, url_for
from flask_login import login_user
from models import db, User

class Signup:
    def post(self):
        # Get data from signup form and assign them to instance variables
        self.firstName = request.form.get('firstName')
        self.lastName = request.form.get('lastName')
        self.email = request.form.get('email')
        self.newPassword = request.form.get('newPassword')

        # Check if any fields are empty
        if not self.firstName or not self.lastName or not self.email or not self.newPassword:
            flash('Please enter all fields', 'Error')
            return redirect(url_for('home'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=self.email).first()
        if existing_user:
            flash('A user with the same Email or Mobile already exists', 'Error')
            return redirect(url_for('home'))

        # Create a new user
        user = User(
            firstName=self.firstName,
            lastName=self.lastName,
            email=self.email,
            password=self.newPassword
        )

        # Add user to the database
        db.session.add(user)
        db.session.commit()

        # Log the user in immediately after signup, if desired
        login_user(user)

        flash('Account created successfully!', 'Success')
