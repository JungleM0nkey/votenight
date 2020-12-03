#!/usr/bin/env python3 

from flask_wtf import FlaskForm,  RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In', id='submit-button')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=64)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email("This field requires a valid email address")])
    invite_code = StringField('Invite Code', validators=[DataRequired()])
    submit = SubmitField('Register', id='submit-button')

class ProfilePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(max=64)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(max=64)])
    new_password_confirm = PasswordField('Confirm new Password', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Change Password', id='submit-button-pw')
    
class ProfileEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email("This field requires a valid email address")])
    submit = SubmitField('Change Email', id='submit-button-email')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email("This field requires a valid email address")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')