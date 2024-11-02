# Main Flask application file

from flask import Flask

app = Flask(__name__)    # initialises the application            

@app.route("/")    # Route for home page
def home():
    return "hello how are you"

if __name__ == "__main__":
    app.run(debug=True)