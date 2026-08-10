from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile

INPUT_CLASSES = (
    "w-full rounded-lg border border-line-strong bg-white px-3 py-2 "
    "text-ink placeholder-muted focus:outline-none focus:ring-2 "
    "focus:ring-brand/40 focus:border-brand"
)


class UserModelFormCreate(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["first_name", "username", "email", "password"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Nombre"}
            ),
            "username": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Nombre de usuario"}
            ),
            "email": forms.EmailInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Correo electrónico"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": INPUT_CLASSES, "placeholder": "Contraseña"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label="Nombre del usuario",
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "Nombre de usuario"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASSES, "placeholder": "Contraseña"}
        ),
        label="Contraseña",
    )
