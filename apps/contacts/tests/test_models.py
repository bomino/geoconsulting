import pytest

from apps.contacts.factories import ContactAssignmentFactory, ContactFactory
from apps.contacts.models import Contact, ContactAssignment
from apps.core.enums import ContactStatus


@pytest.mark.django_db
class TestContact:
    def test_default_status_pending(self):
        contact = ContactFactory()
        assert contact.status == ContactStatus.PENDING

    def test_ordering_newest_first(self):
        c1 = ContactFactory()
        c2 = ContactFactory()
        result = list(Contact.objects.all())
        assert result[0] == c2

    def test_assignment_cascade_on_delete(self):
        assignment = ContactAssignmentFactory()
        contact_pk = assignment.contact.pk
        assignment.contact.delete()
        assert not ContactAssignment.objects.filter(contact_id=contact_pk).exists()
