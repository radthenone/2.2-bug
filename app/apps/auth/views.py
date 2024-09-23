from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import LoginForm, RegisterForm


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("auth:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy("home")
