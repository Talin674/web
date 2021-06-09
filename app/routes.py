from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template("main.html", title="Главная")

@app.route("/user")
def user():
    user = {"user_name":"alex"}
    return render_template("user.html", title="Имя", user=user)

@app.route("/posts")
def posts():
    posts = [
        {"author":{"user_name":"Сократ"},
        "body":"я знаю, что ничего не знаю"},
        {"author": {"user_name": "Марк Твен"},
         "body": "я никогда не позволял школе вмешиаться в моё образование"},
        {"author": {"user_name": "Джон Ленон"},
         "body": "жизнь - это то, что с тобой происходит, пока ты стришь планы"}
    ]
    return render_template("posts.html", title="Цитаты", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Пользователь {} успешно зашёл в систему".format(form.username.data))
        return redirect(url_for("index"))
    return render_template("login.html", title="Логин", form=form)

@app.route("/account")
def account():
    messages = [
        {"author": {"user_name":"alex"},
         "body": "Сегодня хоршая погода!"},
        {"author": {"user_name":"alex"},
         "body": "Всем спокойной ночи!"},
        {"author": {"user_name": "alex"},
         "body": "Всем доброе утро!"},
    ]
    return render_template("account.html", title="Ваш профиль", messages=messages)