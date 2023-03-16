from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    #content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField("Content", validators=[DataRequired()])
    author = StringField('Author')
    slug = StringField('Slugfield', validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form class
class NamerForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a password class
class PasswordForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password_hash = PasswordField("What password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a user form class
class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    favourite_color = StringField("Favourite color")
    about_author = TextAreaField("about_author")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo("password_hash2", message="PAsswords much match")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")

# Update user form class
class UpdateUserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    about_author = TextAreaField("about_author")
    email = StringField('email', validators=[DataRequired()])
    favourite_color = StringField("Favourite color")
    password_hash = PasswordField("Password")
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField("Submit")