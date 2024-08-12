from django.db.models.signals import post_save
from django.dispatch import receiver

from habit.models import HabitInstance
from scoring.models import UserScore


@receiver(post_save, sender=HabitInstance)
def update_user_score(sender, instance, **kwargs):
    if instance.is_completed():
        user_score, created = UserScore.objects.get_or_create(user=instance.user)
        user_score.add_points(instance.habit.score)
