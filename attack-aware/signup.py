from flask import request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash  # Ensure password is hashed before storing it
from models import db, User
from datetime import datetime
from utils import convertBirthday
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder": "First Name", "class": "firstName custom-input"})
    lastName = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Last Name", "class": "lastName custom-input"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "email custom-input"})
    newPassword = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "New Password", "class": "newPassword custom-input"})
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD", "class": "birthday custom-input"})  
    submit = SubmitField('Signup', render_kw={"class": "button"})

class Signup:
    def post(self):
        # Get data from signup form
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        newPassword = request.form["newPassword"]
        birthday_str = request.form["birthday"]

        # Convert birthday to datetime object
        birthday = convertBirthday(birthday_str, flash_category='signup')
        if not birthday:
            flash("Invalid birthday format. Please enter in YYYY-MM-DD format.", 'signup')
            return redirect(url_for('home'))  # Redirect if conversion fails

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists.", 'signup')
            return redirect(url_for('home'))

        # Create and save new user to database
        user = User(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=generate_password_hash(newPassword),  # Secure password storage
            birthday=birthday
        )
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please login.", 'signup')
        return redirect(url_for('home'))

