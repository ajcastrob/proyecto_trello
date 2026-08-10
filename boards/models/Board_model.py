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
