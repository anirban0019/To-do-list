from django.urls import path
from .views import task_list, add_task, update_task, delete_task

urlpatterns = [
    path('tasks/', task_list, name='task-list'),
    path('tasks/add/', add_task, name='add-task'),
    path('tasks/update/<int:pk>/', update_task, name='update-task'),
    path('tasks/delete/<int:pk>/', delete_task, name='delete-task'),
]
