from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateField
from flask_wtf.file import FileField, FileAllowed
from flask import flash, redirect, url_for, request, current_app
from werkzeug.utils import secure_filename, secure_filename
import uuid
import os
from models import db, User
from datetime import datetime
from flask_login import current_user
from utils import convertBirthday


class ProfileForm(FlaskForm):
    firstName = StringField('First Name')
    lastName = StringField('Last Name')
    email = StringField('Email')
    birthday = DateField('Birthday', format='%Y-%m-%d')
    profilePic = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save')

    

def handleProfileUpdate(current_user):
    if 'profilePic' in request.files:
        file = request.files['profilePic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
                print(f"File saved to: {filepath}")  # Debug line to check the path
                current_user.profilePic = filename
                db.session.commit()
                flash('Profile picture updated successfully!', 'update')
                return True
            except Exception as e:
                flash(f"Error saving file: {str(e)}", 'error')
                print(f"Error saving file: {str(e)}")  # Log error
    return False


def allowed_file(filename):
    """Check if the file extension is allowed."""
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

class UpdateProfile:
    def post(self):
        form = ProfileForm()  # Initialize the form instance

        if form.validate_on_submit():  # Check if the form is valid
            # Grab data from Profile form
            firstName = form.firstName.data
            lastName = form.lastName.data
            email = form.email.data
            birthday_str = form.birthday.data

            # Convert the birthday string to a date object
            birthday = convertBirthday(birthday_str, flash_category='update')
            if not birthday:
                flash("Invalid birthday", 'update')
                return redirect(url_for('profile'))  # Redirect if conversion failed
            
            # Retrieve the current user from the database
            user = User.query.get(current_user.id)
            if not user:
                flash("User not found.", 'update')
                return redirect(url_for('profile'))

            # Update the user details
            user.firstName = firstName
            user.lastName = lastName
            user.email = email
            user.birthday = birthday

            # Handle profile picture update (if any)
            if form.profilePic.data:  # Check if a new file is uploaded
                file = form.profilePic.data
                #Generate unique filename using UUID
                #This allows user with same name files to upload an img
                #without any erros
                file_extension = file.filename.rsplit('.', 1)[1].lower()  # Get file extension
                unique_filename = f"{uuid.uuid1()}_{secure_filename(file.filename)}"

                if file and allowed_file(file.filename):
                    # Define the full file path (including the folder path)
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(filepath)

                    user.profilePic = filepath  # Save the filename in the user model

            # Commit changes to the database
            db.session.commit()

            flash("Account updated successfully!", 'update')
            return redirect(url_for('profile'))

        else:
            # Log the form errors to the console for debugging
            print("Form validation failed")
            print(form.errors)  # Log the validation errors
            flash(f"Form validation failed: {form.errors}", 'update')
            return redirect(url_for('profile'))