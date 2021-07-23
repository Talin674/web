# -*- coding: utf-8 -*-
from app import app
from flask import render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread

def send_async_email(app, sender, recipients, msg, server):
    with app.app_context():
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()


def send_email(subject, sender, recipients, text_body, html_body):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    msg.attach(part1)
    msg.attach(part2)
    server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    server.starttls()
    server.login(sender, app.config['MAIL_PASSWORD'])
    Thread(target=send_async_email, args=(app, sender, recipients, msg, server)).start()


# def send_email(subject, sender, recipients, text_body, html_body):
# msg = Message(subject, sender=sender, recipients=recipients)
# msg.body = text_body
# msg.html = html_body
# Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Востановление пароля', sender=app.config['ADMINS'][0], recipients=user.email,
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
