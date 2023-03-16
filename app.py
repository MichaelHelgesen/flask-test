from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, logout_user, login_required, current_user
from webforms import LoginForm, SearchForm, PostForm, UserForm, PasswordForm, NamerForm, UpdateUserForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os

app = Flask(__name__)
ckeditor = CKEditor(app)
# add database
# old sqlite3 app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Hannemin25@localhost/our_users"
# secret key
app.config["SECRET_KEY"] = "super secret key"

UPLOAD_FOLDER = "static/images/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# JSON thing
@app.route("/date")
def get_current_date():
    return {
        "Date": date.today()
    }


# Update Database record
@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    form = UpdateUserForm()
    our_users = Users.query.order_by(Users.date_added)
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        password = request.form["password_hash"]
        if password:
            hashed_pw = generate_password_hash(password, "sha256")
            name_to_update.password_hash = hashed_pw
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.about_author = request.form["about_author"]
        name_to_update.favourite_color = request.form["favourite_color"]
        name_to_update.username = request.form["username"]
        try:
            db.session.commit()
            flash("User updated!")
            return render_template("update_user.html", form=form, name_to_update=name_to_update, our_users=our_users)
        except:
            flash("Error")
            return render_template("update_user.html", form=form, name_to_update=name_to_update, our_users=our_users)
    else:
        return render_template("update_user.html", form=form, name_to_update=name_to_update, our_users=our_users, id=id)


@app.route('/')
def index():
    favourite_animals = ["dog", "cat", "horse"]
    return render_template("index.html", animals=favourite_animals)


@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 15:
        return render_template("admin.html")
    else:
        flash("Must be admin")
        return redirect(url_for("dashboard"))


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    if id == current_user.id:
        users_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()
        try:
            db.session.delete(users_to_delete)
            db.session.commit()
            flash("User deleted")
            our_users = Users.query.order_by(Users.date_added)
            return render_template("add_user.html", form=form, name=name, our_users=our_users)
        except:
            flash("There was a problem")
            our_users = Users.query.order_by(Users.date_added)
            return render_template("add_user.html", form=form, name=name, our_users=our_users)
    else:
        flash("not logged in")
        return redirect(url_for("dashboard"))

@app.route("/add-post", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(
            title=form.title.data,
            poster_id=poster,
            content=form.content.data,
            slug=form.slug.data
        )
        form.title.data = ""
        form.content.data = ""
        # form.author.data = ""
        form.slug.data = ""
        db.session.add(post)
        db.session.commit()
        flash("post submitted")
    return render_template("add_post.html", form=form)


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
            hashed_pw = generate_password_hash(
                form.password_hash.data, "sha256")
            user = Users(name=form.name.data, about_author=form.about_author.data, email=form.email.data,
                         favourite_color=form.favourite_color.data, password_hash=hashed_pw, username=form.username.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.about_author.data = ""
        form.favourite_color.data = ""
        form.password_hash.data = ""
        form.username.data = ""
        flash("User added!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# create name page


@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Name registered")
    return render_template("name.html", name=name, form=form)

# create test page


@app.route("/test", methods=["GET", "POST"])
def test():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ""
        form.password_hash.data = ""
        pw_to_check = Users.query.filter_by(email=email).first()
        # check passw
        passed = check_password_hash(pw_to_check.password_hash, password)
    return render_template("test.html", passed=passed, pw_to_check=pw_to_check, form=form, email=email, password=password)

# Create custom Error Pages
# Invalid URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal server error


@app.errorhandler(500)
def page_error(e):
    return render_template("500.html"), 500


@app.route("/posts")
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", post=posts)


@app.route('/posts/<int:id>')
def blogpost(id):
    post = Posts.query.get_or_404(id)
    return render_template("blogpost.html", post=post)


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post_searched = form.searched.data
        posts = posts.filter(Posts.content.like("%" + post_searched + "%"))
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html",
                               form=form,
                               searched=post_searched,
                               posts=posts
                               )
    return render_template("search.html")


@app.route('/posts/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("post updatet")
        return redirect(url_for("blogpost", id=post.id))

    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template("edit_post.html", form=form)
    else:
        flash("not authorized")
        return redirect(url_for("posts"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("login!")
                return redirect(url_for("dashboard"))
            else:
                flash("wrong password")
        else:
            flash("no such user")
    return render_template("login.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UpdateUserForm()
    id = current_user.id
    our_users = Users.query.order_by(Users.date_added)
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        password = request.form["password_hash"]
        if password:
            hashed_pw = generate_password_hash(password, "sha256")
            name_to_update.password_hash = hashed_pw
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.about_author = request.form["about_author"]
        name_to_update.favourite_color = request.form["favourite_color"]
        name_to_update.username = request.form["username"]
        name_to_update.profile_pic = request.files["profile_pic"]
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save That Image
            saver = request.files['profile_pic']

            # Change it to a string to save to db
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully!")
                return render_template("dashboard.html",
                                       form=form,
                                       name_to_update=name_to_update)
            except:
                flash("Error!  Looks like there was a problem...try again!")
                return render_template("dashboard.html",
                                       form=form,
                                       name_to_update=name_to_update)
        else:
            db.session.commit()
            flash("User updated!")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update, our_users=our_users)


    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, our_users=our_users, id=id)
    

@app.route("/posts/delete/<int:id>", methods=["GET", "POSTS"])
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post.poster.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("blogpost deleted")
            posts = Posts.query.order_by(Posts.date_posted)
            return redirect(url_for("posts", posts=posts))
        except:
            flash("error")
            posts = Posts.query.order_by(Posts.date_posted)
            return redirect(url_for("posts", posts=posts))
    else:
        flash("error")
        posts = Posts.query.order_by(Posts.date_posted)
        return redirect(url_for("posts", posts=posts))
    # return render_template("dashboard.html")

# logout


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("loged out")
    return redirect(url_for("login"))


# Create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # foreign key to link to users (refer to primary key of user)
    poster_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"))  # tabeller i små bokstaver

    # Create database model


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    favourite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    about_author = db.Column(db.Text(500), nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    posts = db.relationship("Posts", backref="poster")  # Referanse til classe
    # password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Create string

    def __repr__(self):
        return '<Name %r>' % self.name
