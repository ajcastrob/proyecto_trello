from django.db import models


class BoardQuerySet(models.QuerySet):
    def accessible_by(self, user):
        # Hoy: solo el owner del board.
        # Con BoardMembership: .filter(Q(owner=user) | Q(memberships__user=user)).distinct()
        return self.filter(owner=user)


class TaskListQuerySet(models.QuerySet):
    def accessible_by(self, user):
        # Una lista es accesible si su board lo es.
        return self.filter(board__owner=user)


class TaskQuerySet(models.QuerySet):
    def accessible_by(self, user):
        # Una tarea es accesible si lo es la lista que la contiene (y su board).
        return self.filter(task_list__board__owner=user)
