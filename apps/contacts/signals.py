from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.contacts.models import Contact


@receiver(post_save, sender=Contact)
def on_contact_created(sender, instance, created, **kwargs):
    if created:
        from apps.core.services import send_notification
        from apps.crm.services import auto_assign_contact

        auto_assign_contact(instance)
        send_notification(
            subject=f"Nouveau contact: {instance.subject or instance.name}",
            template_name="new_contact",
            context={"contact": instance},
        )
