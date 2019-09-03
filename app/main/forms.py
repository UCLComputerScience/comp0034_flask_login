from flask_wtf import FlaskForm
from wtforms import StringField


class SearchForm(FlaskForm):
    term = StringField('Search term')


"""
Form moved to auth

class SignupForm(FlaskForm):
    # Flask-WTF, fields for the signup form with validators
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
"""
