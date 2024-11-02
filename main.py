# Main Flask application file

from flask import Flask, render_template

app = Flask(__name__)    # Initialises the application            

@app.route("/")    # Route for home page URL
def home():
    return render_template("index.html") # Renders the HTML file from templates

if __name__ == "__main__":
    app.run(debug=True)  # Enables debug mode