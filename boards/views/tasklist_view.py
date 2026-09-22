from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from boards.forms import TaskListCreateForm
from boards.models import TaskList, Board, Task
from django.shortcuts import get_object_or_404


@method_decorator(login_required, name="dispatch")
class TaskListDetailView(DetailView):
    model = TaskList
    template_name = "tasklist/tasklist_detail.html"
    context_object_name = "tasklist"

    def get_queryset(self):
        return TaskList.objects.accessible_by(self.request.user).prefetch_related(
            Prefetch(
                "tasks",
                queryset=Task.objects.order_by("position").prefetch_related("labels"),
            )
        )


@method_decorator(login_required, name="dispatch")
class TaskListCreateView(CreateView):
    model = TaskList
    form_class = TaskListCreateForm
    template_name = "tasklist/tasklist_create.html"

    def get_board(self):
        if not hasattr(self, "_board"):
            self._board = get_object_or_404(
                Board.objects.accessible_by(self.request.user),
                pk=self.kwargs["board_pk"],
            )
        return self._board

    def dispatch(self, request, *args, **kwargs):
        # 404 temprano si el board no es del usuario: cubre GET y POST
        self.get_board()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.get_board()
        return context

    def form_valid(self, form):
        board = self.get_board()
        form.instance.board = board
        form.instance.position = board.lists.count() + 1

        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.INFO,
            "Nueva lista ha sido creada con éxito",
        )
        return response

    def get_success_url(self):
        return reverse("board:detail", kwargs={"pk": self.kwargs["board_pk"]})


@method_decorator(login_required, name="dispatch")
class TaskListUpdateView(UpdateView):
    model = TaskList
    form_class = TaskListCreateForm
    template_name = "tasklist/tasklist_update.html"
    context_object_name = "tasklist"

    def get_queryset(self):
        return TaskList.objects.accessible_by(self.request.user).select_related(
            "board"
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.INFO,
            "Título lista ha sido editado con éxito",
        )
        return response

    def get_success_url(self):
        return reverse("board:detail", kwargs={"pk": self.object.board_id})


@method_decorator(login_required, name="dispatch")
class TaskListDeleteView(SuccessMessageMixin, DeleteView):
    model = TaskList
    template_name = "tasklist/tasklist_confirm_delete.html"
    context_object_name = "tasklist"

    def get_queryset(self):
        return TaskList.objects.accessible_by(self.request.user).select_related(
            "board"
        )

    def form_valid(self, form):
        self._board_pk = self.object.board_id
        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.WARNING,
            "Lista ha sido eliminada",
        )
        return response

    def get_success_url(self):
        return reverse("board:detail", kwargs={"pk": self._board_pk})
