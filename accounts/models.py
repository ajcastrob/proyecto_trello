from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    username = models.CharField(
        unique=True, verbose_name="nombre de usuario", max_length=50
    )
    email = models.EmailField(
        verbose_name="email", unique=True, null=False, blank=False
    )
    profile_picture = models.ImageField(
        verbose_name="Foto de perfil",
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )
    bio = models.TextField(verbose_name="biografía", max_length=500, blank=True)
    birth_date = models.DateField(
        verbose_name="Fecha de nacimiento", null=True, blank=True
    )

    def __str__(self):
        return self.email
