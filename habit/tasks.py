import os

from celery import shared_task
from rest_framework import exceptions

from .models import HabitInstance, WorkSession, Reminder, PushNotificationToken

from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests
import json


@shared_task
def send_habit_task(habit_instance_id):
    try:
        habit_instance: HabitInstance = HabitInstance.objects.get(id=habit_instance_id)
        if habit_instance.is_completed():
            return

        if WorkSession.objects.filter(user=habit_instance.user, end_time=None).exists():
            send_habit_notification(habit_instance)
            habit_instance.status = HabitInstance.STATUS.NOTIFIED
            habit_instance.save()

    except HabitInstance.DoesNotExist:
        pass


@shared_task
def send_reminder_task(reminder_id):
    try:
        reminder_instance: Reminder = Reminder.objects.get(id=reminder_id)

        if WorkSession.objects.filter(user=reminder_instance.user_creator, end_time=None).exists():
            send_reminder_notification(reminder_instance)

    except Reminder.DoesNotExist:
        pass


def generate_firebase_auth_key():
    scopes = ['https://www.googleapis.com/auth/firebase.messaging']

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'doost-8726b-ae37069f8ded.json')

    with open(json_path, 'r') as f:
        credentials_info = json.load(f)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=scopes
    )

    credentials.refresh(Request())

    access_token = credentials.token
    return access_token


def send_push_notification(auth_token, token, title, body, habit_id=None, habit_instance=None):
    url = "https://fcm.googleapis.com/v1/projects/doost-8726b/messages:send"

    payload = json.dumps({
        "message": {
            "token": f'{token.fcm_token}',
            "data": {
                "habit_id": f'{habit_id}',
                "title": f'{title}',
                "body": f'{body}',
                "click_action": "/homepage",
                "habit_instance": f'{habit_instance}'
            },
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        error_data = response.json()
        if 'error' in error_data and error_data['error']['details'][0]['errorCode'] == 'UNREGISTERED':
            token.delete()

    print(response.content)


def send_reminder_notification(reminder_instance):
    try:
        user = reminder_instance.user_creator
        title = f'یادآوری {reminder_instance.name}'
        body = f'{reminder_instance.notif_body}'
        access_token = generate_firebase_auth_key()
        target_browsers = PushNotificationToken.objects.filter(owner=user)
        for fcm_token in target_browsers:
            send_push_notification(access_token, fcm_token, title, body)
    except Exception as e:
        raise exceptions.APIException(f'An error occurred while sending notification: {e}')


def send_habit_notification(habit_instance):
    try:
        user = habit_instance.user
        title = f'عادت {habit_instance.habit.name}'
        body = f'{habit_instance.habit.notif_body}'
        access_token = generate_firebase_auth_key()
        target_browsers = PushNotificationToken.objects.filter(owner=user)
        for fcm_token in target_browsers:
            send_push_notification(access_token, fcm_token, title, body, habit_instance.habit.id, habit_instance.id)
    except Exception as e:
        raise exceptions.APIException(f'An error occurred while sending notification: {e}')
