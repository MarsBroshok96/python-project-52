from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError
from task_manager.general_models import TimestampedModel


class Label(TimestampedModel):
    """A label that can be assigned to a task."""
    name = models.CharField(max_length=255,
                            verbose_name=_('Name'),
                            blank=False,
                            error_messages={"blank": _("Name is required")}
                            )

    def delete(self, *args, **kwargs):
        if self.tasks.exists():
            raise ProtectedError("", self)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')

    def __str__(self):
        return self.name
