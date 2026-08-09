from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import UserProfile


# Con AUTH_USER_MODEL personalizado, auth.User NO está registrado en el admin.
# Solo Group viene registrado por defecto; lo re-registramos con Unfold.
admin.site.unregister(Group)


@admin.register(UserProfile)
class UserProfileAdmin(BaseUserAdmin, ModelAdmin):
    """Admin de usuario custom + estilos de Unfold."""

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("username", "pk", "email", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    # Campos extra del perfil (AbstractUser ya trae username, email, etc.)
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Perfil",
            {"fields": ("profile_picture", "bio", "birth_date")},
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Perfil",
            {"fields": ("email", "profile_picture", "bio", "birth_date")},
        ),
    )


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
