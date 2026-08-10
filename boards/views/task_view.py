from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from boards.forms import TaskCreateForm
from boards.models import Task, TaskList


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "board/task_create.html"

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
        return reverse("tasklist_detail", kwargs={"pk": self.kwargs["list_pk"]})


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "board/task_update.html"
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
        return reverse("tasklist_detail", kwargs={"pk": self.object.task_list_id})


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "board/task_confirm_delete.html"
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
        return reverse("tasklist_detail", kwargs={"pk": self.object.task_list_id})
