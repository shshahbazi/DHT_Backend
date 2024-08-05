from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(SingleHabit)
admin.site.register(RecurringHabit)
admin.site.register(HabitInstance)
admin.site.register(WorkSession)
