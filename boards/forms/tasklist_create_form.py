from django import forms
from .constants import INPUT_CLASSES
from boards.models import TaskList


class TaskListCreateForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ["title"]
        labels = {"title": "Nombre de la lista"}
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Ej. Por hacer, En progreso…",
                    "aria-label": "Nombre de la lista",
                    "autocomplete": "off",
                }
            )
        }
