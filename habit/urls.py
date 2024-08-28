from django.urls import path

from habit.views import WorkSessionStartApi, WorkSessionEndApi, EndHabitInstanceApi, CreateSingleHabitApi, \
    CreateRecurringHabitApi, RecurringHabitDetailApi, SingleHabitDetailApi, UserHabitsListApi, AddToDoItemApi, \
    ToDoItemDetailApi, GetToDoListApi

urlpatterns = [
    path('start-work/', WorkSessionStartApi.as_view(), name='start_work'),
    path('end-work/', WorkSessionEndApi.as_view(), name='end_work'),
    path('end-habit/<int:habit_instance_id>/', EndHabitInstanceApi.as_view(), name='end_habit'),

    path('single/create/', CreateSingleHabitApi.as_view(), name='single_create_habit'),
    path('single/<int:habit_id>/detail/', SingleHabitDetailApi.as_view(), name='single_detail_habit'),
    path('recurring/create/', CreateRecurringHabitApi.as_view(), name='recurring_habit_create'),
    path('recurring/<int:habit_id>/detail/', RecurringHabitDetailApi.as_view(), name='recurring_habit'),
    path('user/list/', UserHabitsListApi.as_view(), name='user_list_habits'),

    path('todo/add-item/', AddToDoItemApi.as_view(), name='add_todo_item'),
    path('todo/item/<int:pk>/', ToDoItemDetailApi.as_view(), name='todo_item-detail'),
    path('todo/', GetToDoListApi.as_view(), name='todo_list')

]