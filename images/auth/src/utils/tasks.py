from celery import shared_task
from flask_mail import Message

from flask import current_app

from core.mail import mail
from db.postgres import db
from models.user import User


@shared_task
def send_2_step_verification_code(email, code):
    with current_app.app_context():
        msg = Message(
            'Code for confirm your identity',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email],
        )
        msg.body = f'Code: {code}'
        mail.send(msg)


@shared_task
def send_registration_email_verification_code(email, code):
    with current_app.app_context():
        msg = Message(
            'Code for confirm registration',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email],
        )
        msg.body = f'Code: {code}'
        mail.send(msg)


@shared_task
def send_change_email_verification_code(email, code):
    with current_app.app_context():
        msg = Message(
            'Code for confirm new email',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email],
        )
        msg.body = f'Code: {code}'
        mail.send(msg)


@shared_task
def delete_user_with_not_confirmed_email(user_id):
    user = User.query.get(user_id)
    if user and not user.is_email_confirmed:
        db.session.delete(user)
        db.session.commit()
