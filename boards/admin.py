from django.contrib import admin
from .models import Board, Task, TaskList, Label
from unfold.admin import ModelAdmin


# Register your models here.
@admin.register(Board)
class BoardAdmin(ModelAdmin):
    model = Board
    list_display = ["title", "created_at", "owner"]


@admin.register(TaskList)
class TaskListAdmin(ModelAdmin):
    model = TaskList
    list_display = ["title", "position"]


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    model = Task
    list_display = ["title", "position", "due_date"]
    filter_horizontal = ["labels"]


@admin.register(Label)
class LabelAdmin(ModelAdmin):
    model = Label
    list_display = ["name", "board", "color"]
