from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    rememberMe = BooleanField("Remember Me?")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Repeat Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("This username is not available.")
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError("This email cannot be used.")

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    aboutMe = TextAreaField("About me", validators = [Length(min = 0, max = 128)])
    submit = SubmitField("Save")

    def validate_username(self, username):
        if username.data == current_user.username:
            return
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("This username is not available.")

class PostForm(FlaskForm):
    post = TextAreaField("What's on your mind?", validators = [DataRequired(), Length(min = 1, max = 256)])
    submit = SubmitField("Post")