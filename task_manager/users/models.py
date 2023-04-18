from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Model representing a user."""

    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name=_('first name')
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name=_('last name')
    )

    def __str__(self):
        return self.get_full_name()
