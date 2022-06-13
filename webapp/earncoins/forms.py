from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,\
    SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, InputRequired
from flask import request

"""
def my_length_check(form, field):
    if int(field.data) > 50:
        raise  ValidationError('field  must be less that 50 characters')
    
class MyForm(Form):
    name = StringField('Name', [inputRequired(), my_length_check()])
"""

class CalculatorForm(FlaskForm):
    amount = StringField('Investment amount', validators=[DataRequired(), Length(1, 30)])
    plan = SelectField('Select plan', choices=[
        ((5*(1/100)), 'BEGINNER PLAN'),
        ((10*(1/100)), 'INTERMEDIATE PLAN'),
        ((15*(1/100)), 'ADVANCED PLAN'),
        ((20*(1/100)), 'ENTERPRISE PLAN')
    ])
    submit = SubmitField('Profit')











