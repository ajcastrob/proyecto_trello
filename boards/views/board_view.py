from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from boards.forms import BoardCreateForm
from boards.models import Board, TaskList, Task
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Prefetch
import json


@method_decorator(login_required, name="dispatch")
class BoardListView(ListView):
    template_name = "board/board_list.html"
    model = Board
    context_object_name = "boards"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


@method_decorator(login_required, name="dispatch")
class BoardDetailView(DetailView):
    model = Board
    template_name = "board/board_detail.html"
    context_object_name = "board"

    def get_queryset(self):
        return Board.objects.prefetch_related(
            Prefetch(
                "lists",
                queryset=TaskList.objects.order_by("position").prefetch_related(
                    Prefetch("tasks", queryset=Task.objects.order_by("position"))
                ),
            )
        )


@method_decorator(login_required, name="dispatch")
class BoardCreateView(CreateView):
    model = Board
    form_class = BoardCreateForm
    template_name = "board/board_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user

        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.INFO,
            "Tablero ha sido creado con éxito",
        )
        return response

    def get_success_url(self):
        return reverse("board:detail", kwargs={"pk": self.object.pk})


@method_decorator(login_required, name="dispatch")
class BoardUpdateView(UpdateView):
    model = Board
    form_class = BoardCreateForm
    template_name = "board/board_update.html"
    context_object_name = "boards"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.INFO,
            "Tablero ha sido editado con éxito",
        )
        return response

    def get_success_url(self):
        return reverse("board:detail", kwargs={"pk": self.object.pk})


@method_decorator(login_required, name="dispatch")
class BoardDeleteView(SuccessMessageMixin, DeleteView):
    model = Board
    template_name = "board/board_confirm_delete.html"
    context_object_name = "board"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.WARNING,
            "Tablero ha sido eliminado",
        )
        return response

    def get_success_url(self):
        return reverse("board:list")


@require_POST
def board_reorder(request, pk):

    # Verificar si está logueado
    if not request.user.is_authenticated:
        login_url = settings.LOGIN_URL
        current_path = request.path
        return redirect(f"{login_url}?next={current_path}")

    try:
        data = json.loads(request.body)
        order = data.get("order", [])
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"ok": False, "error": "invalid json"}, status=400)

    for i, list_id in enumerate(order, start=1):
        TaskList.objects.filter(
            pk=list_id, board__owner=request.user, board__pk=pk
        ).update(position=i)

    return JsonResponse({"ok": True})
