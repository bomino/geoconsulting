from django.conf import settings
from django.db import models

from apps.core.enums import TemplateCategory
from apps.core.models import TimestampMixin


class EmailTemplate(TimestampMixin):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    category = models.CharField(max_length=20, choices=TemplateCategory.choices, default=TemplateCategory.CUSTOM)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class AssignmentRule(TimestampMixin):
    name = models.CharField(max_length=255)
    keywords = models.JSONField(help_text="Liste de mots-clés pour l'assignation automatique")
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_rules")
    priority = models.IntegerField(default=0, help_text="Priorité plus élevée = vérifié en premier")
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_rules")

    class Meta:
        ordering = ["-priority"]
