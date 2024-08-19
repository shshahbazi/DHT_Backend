import requests
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.files.base import ContentFile

from user.models import CustomUser, Profile


class SocialAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).
        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data.get('email')
            if email:
                user = CustomUser.objects.get(email__iexact=email.lower())

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        if sociallogin.account.extra_data['email']:
            sociallogin.connect(request, user)

    # def populate_user(self, request, sociallogin, data):
    #     user = sociallogin.user
    #     print(user)
    #     profile = Profile.objects.get(user=user)
    #
    #     user = super().populate_user(request, sociallogin, data)
    #
    #
    #
    #     print(profile)
    # if not profile.picture:
    #     print("1")
    #     github_avatar_url = sociallogin.account.extra_data.get('avatar_url')
    #     if github_avatar_url:
    #         print("2")
    #         response = requests.get(github_avatar_url)
    #         if response.status_code == 200:
    #             print("3")
    #             profile.picture.save(f"{u.username}_github_avatar.jpg", ContentFile(response.content))
    #             profile.save()
