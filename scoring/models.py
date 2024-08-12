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
