from django import forms
from boards.models import Task, TaskList, Board


# Dark stone UI (TaskApp)
INPUT_CLASSES = (
    "w-full rounded-lg bg-stone-950 border border-stone-700 px-3 py-2 "
    "text-stone-100 placeholder-stone-500 focus:outline-none focus:ring-2 "
    "focus:ring-sky-500 focus:border-sky-500"
)


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description"]
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
        }


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


class BoardCreateForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["title", "description"]
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
        }
