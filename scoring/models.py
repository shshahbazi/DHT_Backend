from django.db import models

from user.models import CustomUser


class UserScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def add_points(self, points):
        self.score += points
        self.save()

    def sub_points(self, points):
        self.score = max(self.score - points, 0)
        self.save()


class Reward(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    required_score = models.PositiveIntegerField()

    def is_unlocked(self, user):
        return user.score.score >= self.required_score


class UserReward(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='users')
    unlocked_at = models.DateTimeField(auto_now_add=True)
