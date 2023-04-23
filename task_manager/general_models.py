from django.db import models
from django.utils.translation import gettext_lazy


class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=gettext_lazy('created at')
                                      )
    modified_at = models.DateTimeField(auto_now=True,
                                       verbose_name=gettext_lazy('modified at')
                                       )

    class Meta:
        abstract = True
