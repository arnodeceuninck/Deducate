from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    richting = StringField('Richting', validators=[DataRequired()])
    submit = SubmitField('Verzenden')
