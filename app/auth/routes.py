# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from app.models import User
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email





@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Неверное имя пользователя или пароль'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.rememberme.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template("auth/login.html", title="Логин", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if len(form.username.data) >= 3:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(_('Поздравляем, регисрация прошла успешно!'))
            return redirect(url_for('auth.login'))
        flash(_("Логин должен быть минимум 3 символа"))
    return render_template('auth/registr.html', title='Register', form=form)



@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Проверьте свою электронную почту для получения инструкций по сбросу пароля'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Восстановление пароля', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Ваш пароль был сброшен'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)




