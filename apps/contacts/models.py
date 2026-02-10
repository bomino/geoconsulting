from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from apps.core.enums import ContactStatus


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=320)
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ContactStatus.choices, default=ContactStatus.PENDING)
    notes = models.TextField(blank=True, help_text="Notes internes")
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "archived"]),
            GinIndex(fields=["search_vector"]),
        ]


class ContactAssignment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="assignments")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_contacts")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assignments_made")
    rule = models.ForeignKey("crm.AssignmentRule", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
