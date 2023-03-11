from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    favourite_animals = ["dog", "cat", "horse"]
    return render_template("index.html", animals=favourite_animals)

# localhost:5000/user/
@app.route('/user')
def user():
    first_name = "Mikke"
    return render_template("user.html", first_name=first_name)

# Create custom Error Pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
