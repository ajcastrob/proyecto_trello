from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.edit import DeleteView

from boards.forms import MembershipCreateForm
from boards.models import Board, Membership, Task


@method_decorator(login_required, name="dispatch")
class MembershipCreateView(FormView):
    """Invita por username. Solo el dueno del tablero administra miembros."""

    template_name = "membership/membership_create.html"
    form_class = MembershipCreateForm

    def get_board(self):
        if not hasattr(self, "_board"):
            self._board = get_object_or_404(
                Board.objects.owned_by(self.request.user), pk=self.kwargs["board_pk"]
            )
        return self._board

    def dispatch(self, request, *args, **kwargs):
        # Un miembro no invita: 404 antes de tocar el form (corre en GET y POST)
        self.get_board()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["board"] = self.get_board()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.get_board()
        return context

    def form_valid(self, form):
        membership, created = Membership.objects.get_or_create(
            board=self.get_board(), user=form.user, defaults={"role": "member"}
        )
        if created:
            messages.add_message(
                self.request,
                messages.INFO,
                f"{membership.user.username} ya es miembro del tablero",
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("board:detail", kwargs={"pk": self.get_board().pk})


@method_decorator(login_required, name="dispatch")
class MembershipDeleteView(DeleteView):
    """Saca a un miembro del tablero. El dueno no se puede quitar a si mismo."""

    model = Membership
    template_name = "membership/membership_confirm_delete.html"
    context_object_name = "membership"

    def get_queryset(self):
        return Membership.objects.filter(
            board__owner=self.request.user
        ).select_related("board", "user").exclude(role="owner")

    def form_valid(self, form):
        # Al salir del tablero deja de estar asignado en sus tareas: si no, la
        # tarjeta mostraria un avatar de alguien que ya no puede ver el tablero.
        membership = self.object
        tareas = Task.objects.filter(
            task_list__board=membership.board, assignees=membership.user
        )
        for tarea in tareas:
            tarea.assignees.remove(membership.user)

        username = membership.user.username
        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.WARNING,
            f"{username} ya no es miembro del tablero",
        )
        return response

    def get_success_url(self):
        return reverse("board:detail", kwargs={"pk": self.object.board_id})
