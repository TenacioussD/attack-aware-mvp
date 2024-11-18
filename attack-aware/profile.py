from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed
from flask import flash, redirect, url_for, request, current_app
from werkzeug.utils import secure_filename
import os
from models import db

class ProfileForm(FlaskForm):
    profile_pic = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save')

    

def handleProfileUpdate(current_user):

    #Handles the logic for updating the user's profile picture.

    if 'profilePic' in request.files:
        file = request.files['profilePic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            current_user.profilePic = filename
            db.session.commit()
            flash('Profile picture updated successfully!', 'success')
            return True
    return False

def allowed_file(filename):
    """Check if the file extension is allowed."""
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
