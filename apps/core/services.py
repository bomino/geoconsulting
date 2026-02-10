from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_notification(subject, template_name, context, recipient_list=None):
    if recipient_list is None:
        from apps.accounts.models import User

        recipient_list = list(
            User.objects.filter(is_staff=True, is_active=True).values_list("email", flat=True)
        )

    html_message = render_to_string(f"email/{template_name}.html", context)
    text_message = render_to_string(f"email/{template_name}.txt", context)

    send_mail(
        subject=subject,
        message=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=True,
    )
