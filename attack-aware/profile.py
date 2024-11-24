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
from wtforms.validators import DataRequired, Email, Length


class ProfileForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder": "First Name", "class": "firstName custom-input"})
    lastName = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder": "Last Name", "class": "lastName custom-input"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "email custom-input"})
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD", "class": "birthday custom-input"}) 
    profilePic = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Confirm', render_kw={"class": "confirmButton"})

    

def handleProfileUpdate(current_user):
    if 'profilePic' in request.files:
        file = request.files['profilePic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
                current_user.profilePic = filename
                db.session.commit()
                flash('Profile picture updated successfully!', 'update')
                return True
            except Exception as e:
                flash(f"Error saving file: {str(e)}", 'update')
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
            birthday = form.birthday.data
            profilePic = form.profilePic.data

            if isinstance(birthday, datetime):
                birthday_str = birthday.strftime('%Y-%m-%d')
            else:
                birthday_str = str(birthday)

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
                    user.profilePic = unique_filename  # Save the filename in the user model

            # Commit changes to the database
            db.session.commit()

            flash("Account updated successfully!", 'update')
            return redirect(url_for('profile'))

        else:
            # Log the form errors to the console for debugging
            flash(f"Form validation failed: {form.errors}", 'update')
            return redirect(url_for('profile'))