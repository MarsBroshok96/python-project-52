from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

MSG_SUCCESS_LOGIN = _("You are logged in")
MSG_SUCCESS_LOGOUT = _("You are logged out")


class HomeView(TemplateView):
    "Home page view"
    template_name = "index.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    "User login view"
    next_page = 'homepage'
    success_message = MSG_SUCCESS_LOGIN


class UserLogoutView(LogoutView):
    "User logout view"
    next_page = 'homepage'

    def get(self, request, *args, **kwargs):
        messages.info(request, MSG_SUCCESS_LOGOUT)
        return super().get(request, *args, **kwargs)
