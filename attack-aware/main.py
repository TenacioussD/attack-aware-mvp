# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)  # Initializes the application
app.secret_key = 'attackaware'  # Needed for flashing messages


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
    return redirect(url_for('home')) #Direct to the login page


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

if __name__ == "__main__":
    app.run(debug=True)  # Enables debug mode to rerun the application when changes are made
