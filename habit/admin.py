from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Habit)
admin.site.register(HabitInstance)
admin.site.register(WorkSession)
admin.site.register(UserHabitSuggestion)
