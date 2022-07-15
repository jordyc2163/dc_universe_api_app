from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

class UserSignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    faction = SelectField('Choose Your Faction', choices=[ (1, 'Hero'), (2, 'Villain')], coerce=int)
    submit_button = SubmitField()

class UserSignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()


class SearchCharacterForm(FlaskForm):
    search_char = StringField('Search', validators=None)

