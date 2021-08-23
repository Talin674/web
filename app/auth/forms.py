# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask_babel import lazy_gettext as _l
from flask_babel import _

class LoginForm(FlaskForm):
    username = StringField(_l("Ваше имя:"), validators=[DataRequired()])
    password = PasswordField(_l("Пароль:"), validators=[DataRequired()])
    rememberme = BooleanField(_l("Запомнить меня:"))
    submite = SubmitField(_l("Отправить"))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Ваше имя'), validators=[DataRequired()])
    email = StringField(_l('Почта'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Пароль'), validators=[DataRequired()])
    password2 = PasswordField(_l('Повторите пароль'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Зарегистрироваться'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Пожалуйста, используйте другое имя пользователя'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Пожалуйста, используйте другой адрес электронной почты'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Ваше имя'), validators=[DataRequired()])
    about_me = TextAreaField(_l('Обо мне'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Отправить'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Напишите что-то'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Отправить'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Запросить сброс пароля'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Пароль'), validators=[DataRequired()])
    password2 = PasswordField(_l('Повторите пароль'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Запросить сброя пароля'))