from wtforms import validators, StringField, TextAreaField, SelectField, PasswordField, SubmitField, FileField, RadioField
from flask_wtf import Form
from wtforms.validators import DataRequired, Email


class Comment_Form(Form):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Contact_Form(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')
