from django.db import models

from common.models import BaseModel


class Exercise(BaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to='exercises/', null=True, blank=True)

    def __str__(self):
        return self.name

