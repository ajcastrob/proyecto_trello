from django import forms
from .constants import INPUT_CLASSES
from boards.models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date"]
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
                }
            ),
        }
