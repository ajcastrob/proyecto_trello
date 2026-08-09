from django import forms
from boards.models import Task


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
