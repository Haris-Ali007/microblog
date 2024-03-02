from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
import sqlalchemy as sa
from app.models import User
from app import db

class EditProfileForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    about_me = TextAreaField(label="About me", validators=[Length(min=0, max=140)])
    submit = SubmitField(label="submit")

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username==username.data))
            if user is not None:
                raise ValidationError("Please use a different username")


class EmptyForm(FlaskForm):
    submit = SubmitField(label='Submit')


class PostForm(FlaskForm):
    post = TextAreaField(label='Say something', validators=[
        DataRequired(), Length(min=1, max=140)
    ])
    submit = SubmitField(label='Submit')

