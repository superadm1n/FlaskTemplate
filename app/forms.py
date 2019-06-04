from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from app.models import User


class CustomSelectField(SelectField):
    '''
    This class is overwriting the normal SelectField to disable the prevalidation
    so we can add elements to the list of selections and not have it throw a
    validation error when the form is returned.
    '''

    def pre_validate(self, form):
        pass


class CustomSelectMultipleField(SelectMultipleField):
    '''
    This class is overwriting the normal SelectMultipleField to disable the prevalidation
    so we can add elements to the list of selections and not have it throw a
    validation error when the form is returned.
    '''

    def pre_validate(self, form):
        pass


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match!')])

    submit = SubmitField('Log In')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken!')

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is already taken!')

