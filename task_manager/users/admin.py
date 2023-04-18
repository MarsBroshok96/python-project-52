from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = SignUpForm
    model = CustomUser
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
