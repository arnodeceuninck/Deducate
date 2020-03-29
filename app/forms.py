from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import *


class RegistrationForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    richting = StringField('Richting', validators=[DataRequired()])
    submit = SubmitField('Verzenden')

    def validate_richting(self, name):
        richting = Richting.query.filter_by(name=name.data).first()
        if richting is None:
            raise ValidationError('De richting bestaat nog niet. Gelieve deze eerst aan te maken.')

class NewRichtingForm(FlaskForm):
    richting = StringField('Richting', validators=[DataRequired()])
    submit = SubmitField('Verzenden')

    def validate_richting(self, name):
        richting = Richting.query.filter_by(name=name.data).first()
        if richting is not None:
            raise ValidationError('De richting bestaat al.')