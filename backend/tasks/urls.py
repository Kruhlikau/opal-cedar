from django.urls import path

from .views import TaskDetailView, TaskListView


urlpatterns = [
    path("api/tasks/", TaskListView.as_view(), name="task-list"),
    path("api/tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
