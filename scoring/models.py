from django.db import models

from user.models import CustomUser


class UserScore(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def add_points(self, points):
        self.score += points
        self.save()

    def sub_points(self, points):
        self.score = max(self.score - points, 0)
        self.save()


class Feature(models.Model):
    FEATURE_TYPE_CHOICES = [
        ('profile', 'Profile'),
        ('habit_limit', 'Habit Limit Increase'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=FEATURE_TYPE_CHOICES)
    description = models.TextField()
    cost = models.PositiveIntegerField()
    habit_increase_amount = models.PositiveIntegerField(default=0)

    def get_feature(self, user):
        if self.type == 'profile':
            user.profile.allowed_change_profile = True
        if self.type == 'habit_limit':
            user.profile.allowed_change_profile += self.habit_increase_amount


class PurchasedFeature(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rewards')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='users')
    unlocked_at = models.DateTimeField(auto_now_add=True)
