from flask_mail import Message
from app import mail
from threading import Thread
from flask import current_app 

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template):
    app = current_app._get_current_object()
    msg = Message(subject, html=template, sender=app.config['MAIL_SENDER'], recipients=[to])
    Thread(target=send_async_email, args=(app, msg)).start()
