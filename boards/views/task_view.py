from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
import json
from boards.forms import TaskCreateForm
from boards.models import Task, TaskList


@method_decorator(login_required, name="dispatch")
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasklist"] = TaskList.objects.select_related("board").get(
            pk=self.kwargs["list_pk"]
        )
        return context

    def form_valid(self, form):
        form.instance.task_list_id = self.kwargs["list_pk"]
        form.instance.position = (
            Task.objects.filter(task_list_id=self.kwargs["list_pk"]).count() + 1
        )

        # Guardar el objeto
        response = super().form_valid(form)

        # Agregar el mensaje de forma manual
        messages.add_message(
            self.request,
            messages.INFO,
            "Nueva tarea ha sido creada con éxito",
        )
        return response

    def get_success_url(self):
        return reverse("tasklist:detail", kwargs={"pk": self.kwargs["list_pk"]})


@method_decorator(login_required, name="dispatch")
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task/task_update.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.select_related("task_list__board")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.INFO,
            "Tarea ha sido editada con éxito",
        )
        return response

    def get_success_url(self):
        return reverse("tasklist:detail", kwargs={"pk": self.object.task_list_id})


@method_decorator(login_required, name="dispatch")
class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "task/task_confirm_delete.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.select_related("task_list__board")

    def form_valid(self, form):
        # Guardar el objeto
        response = super().form_valid(form)

        # Agregar el mensaje de forma manual
        messages.add_message(
            self.request,
            messages.WARNING,
            "Tarea ha sido eliminada",
        )

        return response

    def get_success_url(self):
        return reverse("tasklist:detail", kwargs={"pk": self.object.task_list_id})


@require_POST
def task_reorder(request, pk):
    """Persiste orden de tareas en una lista (y mueve entre listas si vienen de otra)."""

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

    try:
        tasklist = TaskList.objects.get(pk=pk, board__owner=request.user)
    except TaskList.DoesNotExist:
        return JsonResponse({"ok": False, "error": "not found"}, status=404)

    for i, task_id in enumerate(order, start=1):
        # Owner check via board; reasigna task_list para moves cross-list
        Task.objects.filter(
            pk=task_id,
            task_list__board__owner=request.user,
        ).update(task_list_id=tasklist.pk, position=i)

    return JsonResponse({"ok": True})
