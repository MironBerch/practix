import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
from uuid import UUID

from jinja2 import Environment, select_autoescape
from sqlalchemy.orm import Session

from db.postgres import Template, User, get_db
from models.models import Notification

SMTP_SERVER = environ.get('SMTP_SERVER')
SMTP_PORT = int(environ.get('SMTP_PORT'))
SMTP_USER = environ.get('SMTP_USER')
SMTP_PASSWORD = environ.get('SMTP_PASSWORD')


async def get_user_email_by_id(user_id: UUID) -> str:
    db: Session = next(get_db())
    user: User = db.query(User).get(user_id)
    return user.email


async def get_template_code_by_id(template_id: UUID) -> str:
    db: Session = next(get_db())
    template: Template = db.query(Template).get(template_id)
    return template.code


async def create_template(template_code: str, context: dict) -> str:
    env = Environment(autoescape=select_autoescape(['html', 'xml']))
    template = env.from_string(template_code)
    rendered_html = template.render(context)
    return rendered_html


async def send_email(subject, body_html, body_text, to_email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email

    if body_text:
        text_part = MIMEText(body_text, 'plain')
        msg.attach(text_part)

    if body_html:
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())


async def send_notification(notification: Notification) -> None:
    if notification.user_email is not None:
        to_email = notification.user_email
    else:
        to_email = await get_user_email_by_id(notification.user_id)
    body_html = None
    if notification.template_id:
        template_code = await get_template_code_by_id(notification.template_id)
        body_html = await create_template(
            template_code=template_code,
            context=notification.context,
        )
    await send_email(
        subject=notification.subject,
        body_html=body_html,
        body_text=notification.text,
        to_email=to_email,
    )
