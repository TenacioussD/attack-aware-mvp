# Main Flask application file

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)    # Initialises the application 
app.secret_key = 'attackaware'  # Needed for flashing messages           

@app.route('/')    # Route for home page URL
def home():
    return render_template('home.html') # Renders the HTML file from templates

@app.route('/Login', methods=['POST'])
def subscribe():
    return render_template('login.html') # Render the HTML file (login) from templates/

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')      # Get the email from the form data
    
    if not email or "@" not in email:                      # Error message if emasil is entered incorrectly
        flash("Please enter a valid email address.", "error")
        return redirect(url_for('home'))
    
    # Add code here to save the email or process the subscription (e.g., save to a database)
    # just flash a message and redirect back to the homepage
    flash("Thank you for subscribing!", "success")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)  # Enables debug mode