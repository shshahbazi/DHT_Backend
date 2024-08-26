from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import BaseModel
from user.models import CustomUser


class DailyMood(BaseModel):
    mood = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='daily_moods')
