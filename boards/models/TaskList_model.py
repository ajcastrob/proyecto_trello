from django.db import models
from .Board_model import Board
from .managers import TaskListQuerySet


class TaskList(models.Model):
    objects = TaskListQuerySet.as_manager()

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(
        max_length=120,
    )
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "lista tarea"
        verbose_name_plural = "lista de tareas"

    def __str__(self):
        return f"{self.board.title} - {self.title}"
