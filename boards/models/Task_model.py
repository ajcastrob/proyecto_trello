from django.db import models
from .TaskList_model import TaskList


class Task(models.Model):
    task_list = models.ForeignKey(
        TaskList, on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(verbose_name="título", max_length=200)
    description = models.TextField(verbose_name="descripción", blank=True)
    position = models.PositiveIntegerField(verbose_name="posición", default=0)
    created_at = models.DateTimeField(
        verbose_name="Fecha de creación", auto_now_add=True
    )

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"

    def __str__(self):
        return self.title
