from flask import request, session, flash, url_for, redirect
from models import db, User
from flask_login import login_user

class Login():
    def post(self):
        email=request.form.get('email') #request data from the login form
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #use email to search for user

        if user.email == email and user.password == password: #if user found via email & password in db
            login_user(user) #set our user as logged in
            flash('Welcome' + user.firstName + '. You logged in successfully')
            return redirect(url_for('threats'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('home'))
 