from flask_wtf import Form
from wtforms import StringField, PasswordField,TextAreaField,DateField,IntegerField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)

from models import Entry


class NewForm(Form):
    title = TextAreaField('title',validators=[DataRequired()])
    date = DateField('date')
    time_spent = IntegerField('time_spent')
    what_you_learned = TextAreaField('what_you_learned')
    resources_to_remember = TextAreaField('resources_to_remember')