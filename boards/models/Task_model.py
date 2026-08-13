from django.db import models
from django.utils import timezone
from .TaskList_model import TaskList

PRIORITY = [
    ("low", "Baja"),
    ("medium", "Media"),
    ("high", "Alta"),
    ("urgent", "Urgente"),
]


class Task(models.Model):
    task_list = models.ForeignKey(
        TaskList, on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(verbose_name="título", max_length=200)
    description = models.TextField(verbose_name="descripción", blank=True)
    position = models.PositiveIntegerField(verbose_name="posición", default=0)
    labels = models.ManyToManyField("Label", blank=True, related_name="tasks")
    priority = models.CharField(
        verbose_name="prioridad", choices=PRIORITY, default="medium", max_length=10
    )
    due_date = models.DateField(verbose_name="Fecha límite", null=True, blank=True)
    created_at = models.DateTimeField(
        verbose_name="Fecha de creación", auto_now_add=True
    )

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"

    def __str__(self):
        return self.title

    # Para comparar con la fecha de hoy
    @property
    def is_overdue(self):
        return bool(self.due_date and self.due_date < timezone.localdate())
