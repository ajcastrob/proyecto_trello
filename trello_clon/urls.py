"""
URL configuration for trello_clon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from trello_clon.views import HomeView, LoginView, RegisterView, logout_view
from boards.views import (
    BoardListView,
    BoardDetailView,
    TaskListDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskListCreateView,
    TaskListUpdateView,
    TaskListDeleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("board/list/", BoardListView.as_view(), name="board_list"),
    path("board/<pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("tasklist/<pk>/", TaskListDetailView.as_view(), name="tasklist_detail"),
    path(
        "tasklist/<int:list_pk>/task/create/",
        TaskCreateView.as_view(),
        name="task_create",
    ),
    path(
        "tasklist/task/delete/<pk>/",
        TaskDeleteView.as_view(),
        name="task_delete",
    ),
    path(
        "tasklist/task/update/<pk>/",
        TaskUpdateView.as_view(),
        name="task_update",
    ),
    path(
        "board/<int:board_pk>/list/create/",
        TaskListCreateView.as_view(),
        name="tasklist_create",
    ),
    path(
        "tasklist/list/update/<pk>/",
        TaskListUpdateView.as_view(),
        name="tasklist_update",
    ),
    path(
        "tasklist/list/delete/<pk>/",
        TaskListDeleteView.as_view(),
        name="tasklist_delete",
    ),
] + debug_toolbar_urls()


# Serve uploaded media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
