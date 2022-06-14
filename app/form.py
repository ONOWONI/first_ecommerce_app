from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from app.models import Product, User
from flask_login import current_user


class UserRegistration(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password')])
    seller = BooleanField('Be a seller')
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email used before, Use another one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('LOG IN')


class AddProduct(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Product Description')
    price = FloatField('Price', validators=[DataRequired()])
    product_pic = FileField('product Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Post')


class UpdateAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    address = TextAreaField('Address', validators=[DataRequired()])
    seller = BooleanField('Become a Seller')
    submit = SubmitField('Update')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('Email used before')


class Buy(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to cart')


class Cash(FlaskForm):
    cash = IntegerField('Ammount', validators=[DataRequired()])
    submit = SubmitField('Deposit')