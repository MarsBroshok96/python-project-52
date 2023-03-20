from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

FIRST_NAME_LABEL = 'First name'
LAST_NAME_LABEL = 'Last name'
EMAIL_HELP_TEXT = 'Enter a valid email address.'
FIRST_NAME_HELP_TEXT = 'Required. Not more than 30 symbols'
LAST_NAME_HELP_TEXT = 'Required. Not more than 30 symbols'
MSG_REGISTERED = 'User successfully registered'


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
