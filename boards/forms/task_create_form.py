from django import forms
from .constants import INPUT_CLASSES
from boards.models import Task


class TaskCreateForm(forms.ModelForm):
    def __init__(self, *args, board=None, **kwargs):
        super().__init__(*args, **kwargs)
        labels = self.fields["labels"]
        if board is not None:
            labels.queryset = labels.queryset.filter(board=board)
        else:
            labels.queryset = labels.queryset.none()

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "labels"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Añade título",
                    "aria-label": "Qué hacer",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Añade un comentario para la tarea",
                    "rows": 5,
                    "aria-label": "Añade comentarios",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": INPUT_CLASSES,
                    "aria-label": "Prioridad",
                }
            ),
            "due_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": INPUT_CLASSES,
                    "type": "date",
                    "aria-label": "Fecha límite",
                },
            ),
            "labels": forms.CheckboxSelectMultiple(),
        }
