from django.urls import path

from ..views import (
    TaskListDetailView,
    TaskListCreateView,
    TaskListUpdateView,
    TaskListDeleteView,
)

app_name = "tasklist"

urlpatterns = [
    path("details/<pk>/", TaskListDetailView.as_view(), name="detail"),
    path("create/<int:board_pk>/", TaskListCreateView.as_view(), name="create"),
    path("update/<pk>/", TaskListUpdateView.as_view(), name="update"),
    path("delete/<pk>/", TaskListDeleteView.as_view(), name="delete"),
]
