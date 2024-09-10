from django.db.models.signals import post_save
from django.dispatch import receiver

from habit.models import ToDoList
from scoring.models import UserScore
from user.models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserScore.objects.create(user=instance)
        ToDoList.objects.create(user=instance)
    else:
        instance.profile.save()
        instance.userscore.save()
        instance.todolist.save()
