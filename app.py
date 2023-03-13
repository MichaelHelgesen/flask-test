from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
#add database
# old sqlite3 app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Hannemin25@localhost/our_users"
# secret key
app.config["SECRET_KEY"] = "super secret key"

db = SQLAlchemy(app)

# Create database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create string
    def __repr__(self):
        return '<Name %r>' % self.name


# Create a form class
class NamerForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a user form class
class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Update Database record
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        try:
            db.session.commit()
            flash("User updated!")
            return render_template("update_user.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error")
            return render_template("update_user.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update_user.html", form=form, name_to_update=name_to_update)

@app.route('/')
def index():
    favourite_animals = ["dog", "cat", "horse"]
    return render_template("index.html", animals=favourite_animals)

# localhost:5000/user/
@app.route('/user/<name>')
def user(name):
    first_name = "Mikke"
    return render_template("user.html", name=name)

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User added!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

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
