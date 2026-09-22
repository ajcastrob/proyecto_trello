from django.conf import settings
from django.db import models
from .Board_model import Board


class Membership(models.Model):
    ROLE = [
        ("owner", "Dueño"),
        ("member", "Miembro"),
    ]

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="board_memberships",
    )
    role = models.CharField(
        verbose_name="rol", max_length=10, choices=ROLE, default="member"
    )
    created_at = models.DateTimeField(
        verbose_name="Fecha de creación", auto_now_add=True
    )

    class Meta:
        verbose_name = "miembro"
        verbose_name_plural = "miembros"
        constraints = [
            models.UniqueConstraint(
                fields=["board", "user"], name="uniq_membership_board_user"
            )
        ]

    def __str__(self):
        return f"{self.board.title} · {self.user}"
