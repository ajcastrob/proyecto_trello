from django.urls import path

from ..views import TaskCreateView, TaskUpdateView, TaskDeleteView, task_reorder

app_name = "task"

urlpatterns = [
    path("create/<int:list_pk>/", TaskCreateView.as_view(), name="create"),
    path("update/<pk>/", TaskUpdateView.as_view(), name="update"),
    path("delete/<pk>/", TaskDeleteView.as_view(), name="delete"),
    path("details/<pk>/reorder/", task_reorder, name="reorder"),
]
