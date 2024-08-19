import requests
from django.core import exceptions
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from user.models import Profile


def send_otp(email, otp):
    try:
        email_body = render_to_string('otp_email_template.html', {'otp_code': otp})
        email = EmailMessage(subject='ورود به دوست', body=email_body, to=[email])
        email.content_subtype = 'html'
        email.send()
    except Exception as e:
        raise exceptions.BadRequest(f'An error occurred while sending email: {e}')

#
# def set_github_avatar(strategy, details, response, socialauth, *args, **kwargs):
#     # Get the user object
#     user = socialauth.user
#
#     # Get the profile or create it if it doesn't exist
#     profile = Profile.objects.get(user=user)
#     print(profile)
#
#     # Check if the profile already has a picture
#     if not profile.picture:
#         github_avatar_url = response.get('avatar_url')
#         if github_avatar_url:
#             response = requests.get(github_avatar_url)
#             if response.status_code == 200:
#                 # Save the picture
#                 content_file = ContentFile(response.content, f"{user.username}_github_avatar.jpg")
#                 profile.picture.save(f"{user.username}_github_avatar.jpg", content_file)
#                 profile.save()
#                 print(profile)
#
