from django.db import models
from .Board_model import Board


COLOR = [
    ("gray", "Gris"),
    ("brand", "Ámbar"),
    ("accent", "Oliva"),
    ("danger", "Rojo"),
]


class Label(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="labels")
    name = models.CharField(verbose_name="nombre", max_length=40)
    color = models.CharField(
        verbose_name="color", max_length=10, choices=COLOR, default="gray"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "name"], name="uniq_label_board_name"
            )
        ]

    def __str__(self):
        return f"{self.board.title} - {self.name}"
