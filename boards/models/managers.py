from django.db import models
from django.db.models import Q


class BoardQuerySet(models.QuerySet):
    def accessible_by(self, user):
        # Quien puede ver y trabajar en el tablero: el dueño y los miembros.
        # El distinct es obligatorio: el join con memberships devuelve una fila
        # por miembro, así que un board con 3 miembros aparecería 3 veces.
        return self.filter(Q(owner=user) | Q(memberships__user=user)).distinct()

    def owned_by(self, user):
        # Quien puede administrar el tablero: editarlo, borrarlo y tocar miembros.
        return self.filter(owner=user)


class TaskListQuerySet(models.QuerySet):
    def accessible_by(self, user):
        # Una lista es accesible si su board lo es (dueño o miembro).
        return self.filter(
            Q(board__owner=user) | Q(board__memberships__user=user)
        ).distinct()


class TaskQuerySet(models.QuerySet):
    def accessible_by(self, user):
        # Una tarea es accesible si lo es la lista que la contiene.
        return self.filter(
            Q(task_list__board__owner=user)
            | Q(task_list__board__memberships__user=user)
        ).distinct()
