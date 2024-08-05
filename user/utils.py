from django.core import exceptions
from django.core.mail import EmailMessage


def send_otp(email, otp):
    try:
        email_body = f'سلام دوست عزیز \nاز کد زیر برای ورود به دوست استفاده کن\n{otp}'
        email = EmailMessage(subject='ورود به دوست', body=email_body, to=[email])
        email.send()
    except Exception as e:
        raise exceptions.BadRequest(f'An error occurred while sending email: {e}')

