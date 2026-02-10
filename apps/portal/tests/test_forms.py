import pytest

from apps.accounts.factories import StaffUserFactory, UserFactory
from apps.portal.factories import ClientProjectFactory
from apps.portal.forms import MessageComposeForm
from apps.projects.factories import ProjectFactory


@pytest.mark.django_db
class TestMessageComposeForm:
    def test_filters_recipients_to_peers_and_staff(self):
        sender = UserFactory()
        peer = UserFactory()
        outsider = UserFactory()
        staff = StaffUserFactory()
        project = ProjectFactory()
        ClientProjectFactory(user=sender, project=project)
        ClientProjectFactory(user=peer, project=project)

        form = MessageComposeForm(sender=sender)
        qs = form.fields["to_user"].queryset
        assert peer in qs
        assert staff in qs
        assert outsider not in qs

    def test_excludes_self(self):
        sender = UserFactory()
        project = ProjectFactory()
        ClientProjectFactory(user=sender, project=project)

        form = MessageComposeForm(sender=sender)
        assert sender not in form.fields["to_user"].queryset

    def test_no_sender_empty_queryset(self):
        form = MessageComposeForm(sender=None)
        assert form.fields["to_user"].queryset.count() == 0

    def test_self_message_rejected(self):
        sender = UserFactory()
        staff = StaffUserFactory()
        project = ProjectFactory()
        ClientProjectFactory(user=sender, project=project)

        form = MessageComposeForm(
            sender=sender,
            data={"to_user": sender.pk, "subject": "Test", "content": "Hi"},
        )
        form.fields["to_user"].queryset = form.fields["to_user"].queryset.model.objects.filter(pk=sender.pk)
        assert not form.is_valid()

    def test_valid_submission(self):
        sender = UserFactory()
        recipient = StaffUserFactory()
        project = ProjectFactory()
        ClientProjectFactory(user=sender, project=project)

        form = MessageComposeForm(
            sender=sender,
            data={"to_user": recipient.pk, "subject": "Test", "content": "Bonjour"},
        )
        assert form.is_valid()
