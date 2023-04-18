from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


User = get_user_model()


class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TimestampedModel):
    """A task that can be assigned to a user."""
    name = models.CharField(max_length=255,
                            verbose_name=_('Name'),
                            blank=False,
                            error_messages={"blank": _("Task name is required")}
                            )
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_('Description')
                                   )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name=_('Executor'),
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        blank=True,
        null=True,
        verbose_name=_('Status')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        blank=True,
        null=True,
    )
    labels = models.ManyToManyField(
        Label,
        related_name='tasks',
        blank=True,
        verbose_name=_('Labels')
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name
