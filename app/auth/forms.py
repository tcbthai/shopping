from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import Length, Email, Regexp, EqualTo, DataRequired
from flask_wtf import Form
from app.models_sqldb import User


class Login_Form(Form):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField()
    submit = SubmitField('Login')


class Register_Form(Form):
    nickname = StringField('Full Name', validators=[DataRequired(), Length(min=6, max=250)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=250), Email()])
    submit = SubmitField('Continue')

    def check_email(self, email):
        user_email = User.query.filter_by(email=email).first()
        if user_email:
            return user_email


class Password_Form(Form):
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')
