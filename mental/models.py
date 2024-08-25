from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DailyMood(models.Model):
    mood = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
