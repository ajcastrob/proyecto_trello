from django.shortcuts import render
from django.views.generic import ListView
from .models import Board


# Create your views here.
class BoardDetailView(ListView):
    template_name = "board/board_detail.html"
    model = Board
    context_object_name = "boards"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)
