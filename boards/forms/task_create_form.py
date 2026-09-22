from django import forms
from accounts.models import UserProfile
from .constants import INPUT_CLASSES
from boards.models import Label, Task


class AssigneesField(forms.ModelMultipleChoiceField):
    """Miembros del tablero que pueden quedar asignados a la tarea.

    El checkbox se etiqueta con `str(objeto)`, y `str(UserProfile)` devuelve el
    email. Eso mostraba el correo de cada miembro del tablero a los demas, asi
    que aca se muestra el username.
    """

    def label_from_instance(self, obj):
        return obj.username


class TaskLabelsField(forms.ModelMultipleChoiceField):
    """`str(Label)` es "tablero - etiqueta". Dentro del form del tablero el
    nombre del tablero es redundante (son todas del mismo), asi que va solo el nombre."""

    def label_from_instance(self, obj):
        return obj.name


class TaskCreateForm(forms.ModelForm):
    labels = TaskLabelsField(
        queryset=Label.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Etiquetas",
    )
    assignees = AssigneesField(
        queryset=UserProfile.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Asignados",
    )

    def __init__(self, *args, board=None, **kwargs):
        super().__init__(*args, **kwargs)

        labels = self.fields["labels"]
        assignees = self.fields["assignees"]
        if board is not None:
            labels.queryset = labels.queryset.filter(board=board)
            # Solo asignables del tablero: Django valida el POST contra este
            # queryset, asi que un pk de otro tablero se rechaza aunque venga a mano.
            assignees.queryset = board.get_assignable_users()
        else:
            labels.queryset = labels.queryset.none()
            assignees.queryset = assignees.queryset.none()

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "labels", "assignees"]
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
        }
