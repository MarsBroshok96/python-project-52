from django.db import models
from django.utils.translation import gettext_lazy
from task_manager.general_models import TimestampedModel


class Status(TimestampedModel):
    "Status model"
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
