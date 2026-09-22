from accounts.models import UserProfile
from django.db import models
from .managers import BoardQuerySet


class Board(models.Model):
    objects = BoardQuerySet.as_manager()

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

    def get_assignable_users(self):
        """Usuarios que pueden quedar asignados a una tarea de este tablero.

        El dueño entra por su membership (la crea la signal al crear el board),
        así los miembros son una sola lista y no dos fuentes.
        """
        return UserProfile.objects.filter(
            board_memberships__board=self
        ).order_by("username")
