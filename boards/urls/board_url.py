from django.urls import path

from ..views import (
    BoardListView,
    BoardDetailView,
    BoardCreateView,
    BoardUpdateView,
    BoardDeleteView,
)

app_name = "board"

urlpatterns = [
    path("", BoardListView.as_view(), name="list"),
    path("details/<pk>/", BoardDetailView.as_view(), name="detail"),
    path("create/", BoardCreateView.as_view(), name="create"),
    path("update/<pk>/", BoardUpdateView.as_view(), name="update"),
    path("delete/<pk>/", BoardDeleteView.as_view(), name="delete"),
]
