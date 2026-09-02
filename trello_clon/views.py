from django.contrib.auth import logout, authenticate, login
from django.urls import reverse, reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.edit import CreateView
from accounts.models import UserProfile
from .forms import LoginForm, UserModelFormCreate
from django.views.decorators.http import require_POST


class HomeView(TemplateView):
    template_name = "core/home.html"


class LoginView(FormView):
    template_name = "core/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(
                self.request, messages.SUCCESS, f"Bienvenido de nuevo, {user.username}"
            )
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(
                self.request, messages.ERROR, "Usuario no válido o contraseña no válida"
            )
            return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    model = UserProfile
    form_class = UserModelFormCreate
    template_name = "core/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):

        # Guardar el objeto
        response = super().form_valid(form)

        # Agregar el mensaje de forma manual
        messages.add_message(
            self.request,
            messages.INFO,
            f"El usuario {self.object.username} ha sido creado con éxito",
        )
        return response


@require_POST
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout con éxito")

    return HttpResponseRedirect(reverse("home"))
