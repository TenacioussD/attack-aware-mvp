# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from signup import Signup, SignupForm
from flask_login import current_user, LoginManager, login_required, logout_user
from login import Login, LoginForm
from admin import Admin
from create_admin import create_initial_admin
from models import db, User, CyberAttack, Scenario
from profile import ProfileForm
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os
from profile import UpdateProfile, ProfileForm, changePassword
from flask import send_from_directory


def create_app():
    app = Flask(__name__)  # Initializes the application
    app.secret_key = 'attackaware'  # Needed for flashing messages
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_profile.db'  # The database that will be created
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit to files to avoid overloads
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # Set the expiration time to 1 hour (in seconds)
    app.config['WTF_CSRF_SECRET_KEY'] = 'another-random-key'

    # Check if the uploads folder exists, create it if it does not
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Initialize the database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
        create_initial_admin()  # Call the function to create the admin

    return app

#create the app by calling the function
app = create_app()

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize the database and login manager
login_manager = LoginManager()

#  # Redirect to the home route for login
login_manager.login_view = 'home'

# Initialize the login manager with the app
login_manager.init_app(app)

# Define ALLOWED_EXTENSIONS globally
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#customisable domain list for email in signup form
allowed_domains = os.getenv('ALLOWED_DOMAINS', 'gmail.com,yahoo.com,outlook.com').split(',')

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    signup_form = SignupForm()

    # Handle the signup form
    if signup_form.validate_on_submit():
        signup_instance = Signup()  # Create an instance of Signup
        return signup_instance.post()

    # Handle the login form
    if login_form.validate_on_submit():
        login_instance = Login()  # Create an instance of Login
        return login_instance.post()

    # Render both forms in the home template
    return render_template('home.html', login_form=login_form, signup_form=signup_form)

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
    return render_template('threats.html')  # Always render the threats page without authentication check

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

# Route to render the contact-us page

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')  # Renders contact us HTML file from templates


from flask import session

@app.route('/admin/attacks', methods=['GET', 'POST'])
def manage_attacks():
    if request.method == 'POST':
        if 'new_attack' in request.form:
            # Add a new attack
            name = request.form['new_attack']
            description = request.form['description']
            prevention = request.form['prevention']
            warning_message = request.form.get('warning_message', '')
            template_name = request.form['template_name']

            # Create and add the new attack to the database
            new_attack = CyberAttack(
                name=name,
                description=description,
                prevention=prevention,
                warning_message=warning_message,
                template_name=template_name
            )
            db.session.add(new_attack)
            db.session.commit()

            flash(f"Attack '{name}' added successfully!", "success")
            session['attack_created'] = True  # Store flag in session

        elif 'scenario-type' in request.form:
            # Add a new scenario
            scenario_type = request.form['scenario-type']
            correct_answer = request.form['correct-answer']
            incorrect_answer = request.form.get('incorrect-answer', '')
            extra_notes = request.form.get('extra-notes', '')

            # Create and add the new scenario to the database
            new_scenario = Scenario(
                type=scenario_type,
                correct_answer=correct_answer,
                incorrect_answer=incorrect_answer,
                extra_notes=extra_notes
            )
            db.session.add(new_scenario)
            db.session.commit()

            flash(f"Scenario '{scenario_type}' added successfully!", "success")
            session['scenario_created'] = True  # Store flag in session

        return redirect(url_for('manage_attacks'))

    # Get all attacks and scenarios from the database
    attacks = CyberAttack.query.all()
    scenarios = Scenario.query.all()

    # Retrieve flags from session and clear them after use
    attack_created = session.pop('attack_created', False)
    scenario_created = session.pop('scenario_created', False)

    # Render the template and pass the flags
    return render_template(
        'manage_attacks.html',
        attacks=attacks,
        scenarios=scenarios,
        attack_created=attack_created,
        scenario_created=scenario_created
    )


@app.route('/attack/<int:attack_id>')
def attack(attack_id):
    attack = CyberAttack.query.get_or_404(attack_id)
    return render_template('attack.html', attack=attack)

@app.route('/admin/remove_attack/<int:attack_id>', methods=['POST'])
def remove_attack(attack_id):
    attack = CyberAttack.query.get_or_404(attack_id)  # Fetch the attack by ID
    db.session.delete(attack)  # Delete the attack from the database
    db.session.commit()  # Commit the changes to the database

    flash(f"Attack '{attack.name}' removed successfully!", "success")  # Flash success message
    return redirect(url_for('manage_attacks'))  # Redirect back to the manage attacks page

@app.route('/remove_scenario/<int:scenario_id>', methods=['POST'])
def remove_scenario(scenario_id):
    scenario = Scenario.query.get(scenario_id)
    if scenario:
        db.session.delete(scenario)
        db.session.commit()
        flash(f"Scenario '{scenario.type}' removed successfully.", "success")
    else:
        flash("Scenario not found.", "error")
    return redirect(url_for('manage_attacks'))


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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    user=current_user

    form = ProfileForm()
    # Check if the form is submitted and validated
    if form.validate_on_submit():
        updateProfile_instance = UpdateProfile()
        return updateProfile_instance.post()

    return render_template('profile.html', form=form, user=user)  # Pass form to template

@app.route('/uploads/<filename>')
def uploadedFile(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)  # Enables debug mode to rerun the application when changes are made

