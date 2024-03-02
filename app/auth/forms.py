from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app.models import User
from app import db

class LoginForm(FlaskForm):
    username = StringField(label="username", validators=[DataRequired()])
    password = PasswordField(label="password", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField(label="Sign In")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username==username.data))
        if user is None:
            raise ValidationError('No such user exists')         


class RegisterationForm(FlaskForm):
    username = StringField(name="Username", validators=[DataRequired()])
    email = StringField(name="Email", validators=[DataRequired(), Email()])
    password = PasswordField(name="Password", validators=[DataRequired()])
    password2 = PasswordField(name="Repeat password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username==username.data))
        if user is not None:
            raise ValidationError('Please use a different user')
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email==email.data))
        if user is not None:
            raise ValidationError('Please use a different email')
