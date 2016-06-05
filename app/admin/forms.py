from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, FileField, IntegerField
from flask_wtf import Form
from wtforms.validators import DataRequired, Length, EqualTo, Email
from app.models_sqldb import User


class CategoriesCreate(Form):
    new_category = StringField('Category Name', validators=[DataRequired(), Length(min=6, max=40)])
    submit = SubmitField('Save')

class PostForm(Form):
    category = SelectField()
    name = StringField('name')
    image = StringField('images')
    description= TextAreaField()
    detail = TextAreaField()
    code= StringField('code')
    price= IntegerField('price')
    stock= IntegerField('In stock')
    submit = SubmitField('Save')
