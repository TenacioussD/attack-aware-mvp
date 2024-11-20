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
            flash(f'Welcome {user.firstName}. You logged in successfully', 'update') #spesify which form the flash message should show up on ('threats')
       
            if user.is_admin:
                flash('Welcome Admin', 'threats')

            return redirect(url_for('threats'))  # Redirect to the home page or dashboard
        else:
            flash('Invalid email or password', 'login') #spesify which form the flash message should show up on ('login')
            return redirect(url_for('home'))
 