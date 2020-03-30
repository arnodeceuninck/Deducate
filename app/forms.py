from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import *

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Richting', validators=[])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    richting = StringField('Richting', validators=[])
    locatie = StringField('Richting', validators=[])
    submit = SubmitField('Verzenden')

    def validate_richting(self, name):
        richting = Richting.query.filter_by(name=name.data).first()
        if richting is None:
            raise ValidationError('De richting bestaat nog niet. Gelieve deze eerst aan te maken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Gelieve een ander emailadres te gebruiken. Er bestaat al iemand met het opgegeven adres.')

class NewRichtingForm(FlaskForm):
    richting = StringField('Richting', validators=[DataRequired()])
    submit = SubmitField('Verzenden')

    def validate_richting(self, name):
        richting = Richting.query.filter_by(name=name.data).first()
        if richting is not None:
            raise ValidationError('De richting bestaat al.')