from django.core import exceptions
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_otp(email, otp):
    try:
        email_body = render_to_string('otp_email_template.html', {'otp_code': otp})
        email = EmailMessage(subject='ورود به دوست', body=email_body, to=[email])
        email.content_subtype = 'html'
        email.send()
    except Exception as e:
        raise exceptions.BadRequest(f'An error occurred while sending email: {e}')

