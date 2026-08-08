from accounts.models import UserProfile
from django.db import models


class Board(models.Model):
    title = models.CharField(verbose_name="Nombre del dashboard", max_length=120)
    description = models.TextField(verbose_name="Descripción", blank=True)
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="owned_boards",
        verbose_name="Dueño del dashboard",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Tablero"
        verbose_name_plural = "Tableros"

    def __str__(self):
        return self.title


class TaskList(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(max_length=120)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "lista tarea"
        verbose_name_plural = "lista de tareas"

    def __str__(self):
        return f"{self.board.title} - {self.title}"


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
