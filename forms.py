from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    surname = StringField("Surname", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

    passwordAgain = PasswordField("PasswordAgain", validators=[DataRequired()])