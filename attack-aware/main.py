from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flask app setup
app = Flask(__name__)  # Initializes the application
app.secret_key = 'attackaware'  # Needed for flashing messages

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attacks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database model for cyberattacks
class CyberAttack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prevention = db.Column(db.Text, nullable=False)
    warning_message = db.Column(db.String(255), nullable=True)
    template_name = db.Column(db.String(100), nullable=False)  # e.g., "ransomware.html"

# Database model for videos
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Video {self.link}>'

# Routes

@app.route('/')  # Route for home page URL decorator
def home():
    return render_template('home.html')  # Renders the HTML file from templates

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')  # Get the email from the form data

    if not email or "@" not in email:  # Error message if email is entered incorrectly
        flash("Please enter a valid email address.", "error")
        return redirect(url_for('home'))

    # Add code here to save the email or process the subscription (e.g., save to a database)
    # just flash a message and redirect back to the homepage currently
    flash("Thank you for subscribing!", "success")
    return redirect(url_for('home'))  # Redirect to the login page

# Route to render the threats page
@app.route('/threats')
def threats():
    return render_template('threats.html')  # This renders HTML file from the templates

# Dynamic route for cyberattacks
@app.route('/admin/attacks', methods=['GET', 'POST'])
def manage_attacks():
    if request.method == 'POST':
        name = request.form['new_attack']
        description = request.form['description']
        prevention = request.form['prevention']
        warning_message = request.form.get('warning_message', '')
        template_name = request.form['template_name']

        # Create a new attack object
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
        return redirect(url_for('manage_attacks'))

    # Get all attacks from the database
    attacks = CyberAttack.query.all()
    return render_template('manage_attacks.html', attacks=attacks)

@app.route('/attack/<int:attack_id>')
def attack(attack_id):
    # Get a single attack by ID
    attack = CyberAttack.query.get_or_404(attack_id)
    return render_template(attack.template_name, attack=attack)

# Routes for individual threats
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
    return render_template('phishing_scams.html')  # Renders phishing scams HTML file from templates

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')  # Renders contact us HTML file from templates

@app.route('/remove_attack/<int:attack_id>', methods=['POST'])
def remove_attack(attack_id):
    attack = CyberAttack.query.get(attack_id)
    if attack:
        db.session.delete(attack)
        db.session.commit()
        flash(f'Attack "{attack.name}" removed successfully.', "success")
    else:
        flash("Attack not found.", "error")
    return redirect(url_for('manage_attacks'))

# Video management routes
@app.route('/manage_videos', methods=['GET', 'POST'])
def manage_videos():
    if request.method == 'POST':
        video_link = request.form['video_link']

        # Create a new video entry
        new_video = Video(link=video_link)
        db.session.add(new_video)
        db.session.commit()
        flash(f"Video '{video_link}' added successfully!", "success")
        return redirect(url_for('manage_videos'))  # Reload the page to show the new video

    # Get all videos from the database
    videos = Video.query.all()

    return render_template('manage_videos.html', videos=videos)

@app.route('/remove_video/<int:video_id>', methods=['POST'])
def remove_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        flash(f"Video '{video.link}' removed successfully.", "success")
    else:
        flash("Video not found.", "error")
    return redirect(url_for('manage_videos'))  # Reload the page to show the updated list

# Initialize database and run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the database tables if they don't exist
    app.run(debug=True)  # Enables debug mode
