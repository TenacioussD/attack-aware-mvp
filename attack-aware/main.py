# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from signup import Signup
from flask_login import current_user, LoginManager, login_required, logout_user
from login import Login
from admin import Admin
from create_admin import create_initial_admin 
from profile import ProfileForm, handleProfileUpdate
from werkzeug.utils import secure_filename
import os

def create_app():
    app = Flask(__name__)  # Initializes the application
    app.secret_key = 'attackaware'  # Needed for flashing messages
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_profile.db'  # The database that will be created
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit to files to avoid overloads


    # Initialize the database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
        create_initial_admin()  # Call the function to create the admin

    return app

#create the app by calling the function
app = create_app()

# Initialize the database and login manager
login_manager = LoginManager()

# Define the login view (this is the page users will be redirected to if they need to log in)
login_manager.login_view = 'login'

# Initialize the login manager with the app
login_manager.init_app(app)

#user loader function for Flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define ALLOWED_EXTENSIONS globally
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'signup':
            signup_instance = Signup()  # Create an instance of Signup
            return signup_instance.post()  # Call the post method on the instance
        
        elif action == 'login':
            login_instance = Login()  # Create an instance of Login
            return login_instance.post()  # Call the post method on the instance

    return render_template('home.html')  # Render the home page template
# Route to render the threats page

@app.route('/make_admin/<int:user_id>', methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        flash("You do not have permission to perform this action.", 'admin')
        return redirect(url_for('home'))
    
    result = Admin.promore_to_admin(user_id)
    flash(result)
    return redirect(url_for('home'))

@app.route('/threats')
def threats():
    user = current_user

    return render_template('threats.html', user=user.id)  # This renders HTML file from the templates
   
# Route to render the ransomware page
@app.route('/ransomware')
def ransomware():
    return render_template('ransomware.html')  # Renders ransomware HTML file from templates

@app.route('/social_engineering')
def social_engineering():
    return render_template('social_engineering.html')  # Renders social engineering HTML file from templates

@app.route('/cyber_hygiene')
def cyber_hygiene():
    return render_template('cyber_hygiene.html')  # Renders cyber hygiene HTML file from templates

@app.route('/IoT')
def IoT():
    return render_template('IoT.html')  # Renders IoT HTML file from templates

@app.route('/phishing_scams')
def phishing_scams():
    return render_template('phishing_scams.html')       # Renders phishing scams HTML file from templates

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    return render_template('profile.html', user=current_user)

# Route to render the contact-us page
@app.route('/contact-us')
def contact():
    return render_template('contact-us.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'login') #let flash pop-up on home login form
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user is None:
        print("User not found")
    return user


if __name__ == "__main__":
    app.run(debug=True)  # Enables debug mode to rerun the application when changes are made

