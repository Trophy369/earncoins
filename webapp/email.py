from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
from flask_login import current_user



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message(app.config['CRYPTOWELL_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#                   sender=app.config['CRYPTOWELL_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr


def send_email(subject, sender, recipients, text_body, html_body):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Earncoins] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_confirmation_email(user):
    token = user.generate_confirmation_token()
    send_email('[Earncoins] Confirm your Email',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm.html',
                                         user=user, token=token))


def send_deposit_email(user):
    send_email('[Earncoins] Deposit',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               # text_body=render_template('email/deposit.txt',
               #                           user=current_user.username),
               html_body=render_template('email/deposit.html',
                                         user=current_user.username))


def send_invest_email(user):
    send_email('[Earncoins] Investment successful',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               # text_body=render_template('email/invest.txt',
               #                           user=current_user.username),
               html_body=render_template('email/invest.html',
                                         user=current_user.username))


def send_share_email(user):
    send_email('[Earncoins] Share balance',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               # text_body=render_template('email/share.txt',
               #                           user=current_user.username),
               html_body=render_template('email/share.html',
                                         user=current_user.username))


def send_withdrawal_email(user):
    send_email('[Earncoins] Withdrawal request',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               # text_body=render_template('email/withdrawal.txt',
               #                           user=current_user.username),
               html_body=render_template('email/withdrawal.html',
                                         user=current_user.username))

