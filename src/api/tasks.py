import smtplib
from email.message import EmailMessage

from src.routes.images import celery

SMTP_PASSWORD = ''
SMTP_USER = ''
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def get_email_template_dashboard(nickname: str):
    email = EmailMessage()
    email['Subject'] = 'your subscription will end soon'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {nickname}, your subscription will end soon.  it will automatically renew if there is money on your card </h1>'
        '<img src="xxx'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
