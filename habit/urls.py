from django.urls import path

from habit.views import WorkSessionStartApi, WorkSessionEndApi, EndHabitInstanceApi, \
    CreateRecurringHabitApi, RecurringHabitDetailApi, UserHabitsListApi, AddToDoItemApi, \
    ToDoItemDetailApi, GetToDoListApi, SubmitUserHabitSuggestionApi, CreateReminderApi, ReminderDetailApi

urlpatterns = [
    path('start-work/', WorkSessionStartApi.as_view(), name='start_work'),
    path('end-work/', WorkSessionEndApi.as_view(), name='end_work'),
    path('end-habit/<int:habit_instance_id>/', EndHabitInstanceApi.as_view(), name='end_habit'),

    path('reminder/create/', CreateReminderApi.as_view(), name='create_reminder'),
    path('reminder/<int:reminder_id>/detail/', ReminderDetailApi.as_view(), name='reminder_detail'),


    path('recurring/create/', CreateRecurringHabitApi.as_view(), name='recurring_habit_create'),
    path('recurring/<int:habit_id>/detail/', RecurringHabitDetailApi.as_view(), name='recurring_habit'),
    path('user/list/', UserHabitsListApi.as_view(), name='user_list_habits'),

    path('todo/add-item/', AddToDoItemApi.as_view(), name='add_todo_item'),
    path('todo/item/<int:pk>/', ToDoItemDetailApi.as_view(), name='todo_item-detail'),
    path('todo/', GetToDoListApi.as_view(), name='todo_list'),

    path('suggest/submit/', SubmitUserHabitSuggestionApi.as_view(), name='user_habit-suggest')

]