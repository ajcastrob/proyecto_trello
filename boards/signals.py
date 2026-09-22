from django.db.models.signals import post_save
from django.dispatch import receiver

from boards.models import Board, Membership


@receiver(post_save, sender=Board)
def create_owner_membership(sender, instance, created, **kwargs):
    """Cada tablero arranca con su dueño como miembro, para que el tablero
    tenga una sola lista de miembros (owner incluido) y no dos fuentes."""
    if created:
        Membership.objects.get_or_create(
            board=instance, user=instance.owner, defaults={"role": "owner"}
        )
