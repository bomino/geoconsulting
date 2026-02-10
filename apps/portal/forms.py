from django import forms
from django.db.models import Q

from apps.portal.models import ClientProject, Message


class MessageComposeForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["to_user", "subject", "content"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "w-full", "placeholder": "Objet du message"}),
            "content": forms.Textarea(attrs={"class": "w-full", "rows": 6, "placeholder": "Votre message..."}),
        }
        labels = {
            "to_user": "Destinataire",
            "subject": "Objet",
            "content": "Message",
        }

    def __init__(self, *args, sender=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = sender
        if sender is None:
            self.fields["to_user"].queryset = self.fields["to_user"].queryset.none()
            return

        from apps.accounts.models import User

        sender_project_ids = ClientProject.objects.filter(
            user=sender
        ).values_list("project_id", flat=True)

        peer_user_ids = ClientProject.objects.filter(
            project_id__in=sender_project_ids
        ).exclude(user=sender).values_list("user_id", flat=True)

        self.fields["to_user"].queryset = User.objects.filter(
            Q(pk__in=peer_user_ids) | Q(is_staff=True)
        ).exclude(pk=sender.pk).distinct()

    def clean_to_user(self):
        to_user = self.cleaned_data["to_user"]
        if self.sender and to_user == self.sender:
            raise forms.ValidationError("Vous ne pouvez pas vous envoyer un message.")
        return to_user
