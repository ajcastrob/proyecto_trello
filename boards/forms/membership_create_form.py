from django import forms

from accounts.models import UserProfile
from .constants import INPUT_CLASSES


class MembershipCreateForm(forms.Form):
    """Invita a un usuario al tablero por su username.

    No es un ModelForm a proposito: el `board` no lo elige quien llena el form,
    lo pone la vista desde la URL, y el rol lo fija el sistema.
    """

    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Ej. ana",
                "aria-label": "Nombre de usuario a invitar",
                "autocomplete": "off",
            }
        ),
    )

    def __init__(self, *args, board=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.user = None

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        try:
            user = UserProfile.objects.get(username__iexact=username)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError("No existe un usuario con ese nombre.")

        if self.board is not None:
            if self.board.owner_id == user.pk:
                raise forms.ValidationError("Ese usuario ya es el dueño del tablero.")
            if self.board.memberships.filter(user=user).exists():
                raise forms.ValidationError("Ese usuario ya es miembro del tablero.")

        self.user = user
        return username
