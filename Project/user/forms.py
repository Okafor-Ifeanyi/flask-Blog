from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from flask_login import current_user
# from Project import db
from Project.models import User


class RegistrationForm(FlaskForm):
    # creating forms and validating user inputs
    username = StringField('Username', 
    validators=[DataRequired(), length(min=2, max=20)])
     
    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
                        validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('The username has already been taken')

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('This email has already been used here')


class LoginForm(FlaskForm):
    # creating forms and validating user inputs
    email = StringField('Email',
             validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    # creating forms and validating user inputs
    username = StringField('Username', 
    validators=[DataRequired(), length(min=2, max=20)])
     
    email = StringField('Email',
            validators=[DataRequired(), Email()])
    
    picture = FileField('Update DP', validators=[FileAllowed(['jpg','png','bmp'])])

    submit = SubmitField('Update Acc..')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError('The username has already been taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('This email has already been used here')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user is None:
            raise ValidationError('This email does not exist Please regsiter')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
