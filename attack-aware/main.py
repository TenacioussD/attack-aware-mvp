# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from signup import Signup
from flask_login import current_user

def create_app():
    app = Flask(__name__)  # Initializes the application
    app.secret_key = 'attackaware'  # Needed for flashing messages
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # The database that will be created
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist

    return app



#create the app by calling the function
app = create_app()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'signup':
            signup_instance = Signup()
            result = signup_instance.post()  # Capture the result from post()

            # After handling the signup, redirect to avoid resubmission upon refresh
            if result:  # Check if signup was successful
                flash("Signup successful!")
                return redirect(url_for('home'))  # Redirect to the 'threats' page (or another page)

            # If signup failed, flash an error message
            flash("Signup failed! Please try again.")
            return redirect(url_for('home'))  # Redirect back to the home page

    return render_template('home.html')  # Render the home page template

# Route to render the threats page
@app.route('/threats')
def threats():
    return render_template('threats.html')  # This renders HTML file from the templates
   
   

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


if __name__ == "__main__":
    app.run(debug=True)  # Enables debug mode to rerun the application when changes are made
