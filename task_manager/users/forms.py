from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


FIRST_NAME_LABEL = _('First name')
LAST_NAME_LABEL = _('Last name')
EMAIL_HELP_TEXT = _('Enter a valid email address.')
FIRST_NAME_HELP_TEXT = _('Required. Not more than 30 symbols')
LAST_NAME_HELP_TEXT = _('Required. Not more than 30 symbols')
MSG_REGISTERED = _('User successfully registered')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=False,
                             help_text=EMAIL_HELP_TEXT)
    first_name = forms.CharField(required=True, max_length=30,
                                 label=FIRST_NAME_LABEL,
                                 help_text=FIRST_NAME_HELP_TEXT)
    last_name = forms.CharField(required=True, max_length=30,
                                label=LAST_NAME_LABEL,
                                help_text=LAST_NAME_HELP_TEXT)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2', 'email')
