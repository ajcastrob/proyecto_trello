from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from boards.forms import BoardCreateForm
from boards.models import Board


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
        return reverse("board_detail", kwargs={"pk": self.object.pk})


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
        return reverse("board_detail", kwargs={"pk": self.object.pk})


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
        return reverse("board_list")
