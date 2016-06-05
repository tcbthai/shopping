from . import mail
from flask import current_app, render_template
from flask_mail import Message


def send_mail(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


def send_contact_mail(email, content, sender_nickname):
    msg = Message(subject=email, sender=sender_nickname, recipients=[current_app.config['FLASKY_ADMIN']])
    msg.body = content
    msg.html = '<b>' + content + '</b>'
    mail.send(msg)
