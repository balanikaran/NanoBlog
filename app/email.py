from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread

def sendAsyncMail(app, msg):
    with app.app_context():
        mail.send(msg)

def sendEmail(subject, sender, recipients, textBody, htmlBody):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = textBody
    msg.html = htmlBody
    Thread(target = sendAsyncMail, args = (app, msg)).start()

def send_password_reset_email(user):
    token = user.getResetPasswordToken()
    sendEmail(
        "[NanoBlog] - Password reset request recieved",
        sender = app.config["ADMINS"][0],
        recipients = [user.email],
        textBody = render_template("email/reset_password_mail_content.txt", user = user, token = token),
        htmlBody = render_template("email/reset_password_mail_content.html", user = user, token = token)
    )