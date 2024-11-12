from flask import request, session, flash, url_for, redirect
from models import db, User
from flask_login import login_user, UserMixin

class Login():
    def post(self):
        email=request.form.get('email') #request data from the login form
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #use email to search for user

        if user and user.check_password(password):  # Use the check_password method created in models.py
            login_user(user)
            flash(f'Welcome {user.firstName}. You logged in successfully')
            return redirect(url_for('threats'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('home'))
 