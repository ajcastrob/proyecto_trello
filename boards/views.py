from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from .models import Board, TaskList, Task
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from boards.forms import TaskCreateForm, TaskListCreateForm


# Create your views here.
class BoardListView(ListView):
    template_name = "board/board_list.html"
    model = Board
    context_object_name = "boards"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


class BoardDetailView(DetailView):
    model = Board
    template_name = "board/board_detail.html"
    context_object_name = "board"

    def get_queryset(self):
        return Board.objects.prefetch_related("lists__tasks")


class TaskListDetailView(DetailView):
    model = TaskList
    template_name = "board/tasklist_detail.html"
    context_object_name = "tasklist"


class TaskListCreateView(CreateView):
    model = TaskList
    form_class = TaskListCreateForm
    template_name = "board/tasklist_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = Board.objects.get(pk=self.kwargs["board_pk"])
        return context

    def form_valid(self, form):
        form.instance.board_id = self.kwargs["board_pk"]
        form.instance.position = (
            TaskList.objects.filter(board_id=self.kwargs["board_pk"]).count() + 1
        )

        response = super().form_valid(form)
        messages.add_message(
            self.request,
            messages.INFO,
            "Nueva lista ha sido creada con éxito",
        )
        return response

    def get_success_url(self):
        return reverse("board_detail", kwargs={"pk": self.kwargs["board_pk"]})


class TaskListUpdateView(UpdateView):
    model = TaskList
    form_class = TaskListCreateForm
    template_name = "board/tasklist_update.html"
    context_object_name = "tasklist"

    def get_queryset(self):
        return TaskList.objects.filter(board__owner=self.request.user).select_related(
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
        return reverse("board_detail", kwargs={"pk": self.object.board_id})


class TaskListDeleteView(SuccessMessageMixin, DeleteView):
    model = TaskList
    template_name = "board/tasklist_confirm_delete.html"
    context_object_name = "tasklist"

    def get_queryset(self):
        return TaskList.objects.filter(board__owner=self.request.user).select_related(
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
        return reverse("board_detail", kwargs={"pk": self._board_pk})


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
