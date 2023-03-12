from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "super secret key"

# Create a form class
class NamerForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def index():
    favourite_animals = ["dog", "cat", "horse"]
    return render_template("index.html", animals=favourite_animals)

# localhost:5000/user/
@app.route('/user/<name>')
def user(name):
    first_name = "Mikke"
    return render_template("user.html", name=name)

#create name page
@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Name registered")
    return render_template("name.html", name=name, form=form)

# Create custom Error Pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_error(e):
    return render_template("500.html"), 500
