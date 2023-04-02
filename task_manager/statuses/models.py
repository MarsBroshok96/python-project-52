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


class Status(TimestampedModel):
    name = models.CharField(verbose_name=gettext_lazy('name'),
                            max_length=55,
                            unique=True,
                            blank=False,
                            )

    class Meta:
        verbose_name = gettext_lazy('status')
        verbose_name_plural = gettext_lazy('statuses')

    def __str__(self):
        return self.name
