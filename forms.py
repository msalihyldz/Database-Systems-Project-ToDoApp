from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, DateField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])

    surname = StringField("Surname", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])

    repeatpassword = PasswordField("Repeat Password", validators=[DataRequired()])

class CreateWorkspaceForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])

    description = StringField("Decription", validators=[DataRequired()])

    color = StringField("Decription", validators=[DataRequired()])

    order = IntegerField("Order", validators=[DataRequired()])


class TaskForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired()])

    endDate = DateField("EndDate")

    categoryId = IntegerField("CategoryId")

    listId = IntegerField("ListId")

    assignedId = IntegerField("AssignedId")
