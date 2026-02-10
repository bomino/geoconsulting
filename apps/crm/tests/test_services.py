from unittest.mock import patch

import pytest

from apps.accounts.factories import UserFactory
from apps.contacts.models import Contact, ContactAssignment
from apps.crm.factories import AssignmentRuleFactory
from apps.crm.services import auto_assign_contact


@pytest.mark.django_db
class TestAutoAssignContact:
    @patch("apps.core.services.send_notification")
    def test_matches_keyword(self, mock_notify):
        user = UserFactory()
        AssignmentRuleFactory(keywords=["devis"], assigned_user=user)
        contact = Contact.objects.create(
            name="Test", email="t@t.com", message="Demande de devis"
        )
        assert ContactAssignment.objects.filter(contact=contact, assigned_to=user).exists()

    @patch("apps.core.services.send_notification")
    def test_no_match_returns_false(self, mock_notify):
        AssignmentRuleFactory(keywords=["hydraulique"])
        contact = Contact.objects.create(
            name="Test", email="t@t.com", subject="General", message="Bonjour"
        )
        assert ContactAssignment.objects.filter(contact=contact).count() == 0

    @patch("apps.core.services.send_notification")
    def test_priority_order(self, mock_notify):
        user_low = UserFactory()
        user_high = UserFactory()
        AssignmentRuleFactory(keywords=["route"], assigned_user=user_low, priority=1)
        AssignmentRuleFactory(keywords=["route"], assigned_user=user_high, priority=10)
        contact = Contact.objects.create(
            name="Test", email="t@t.com", subject="Projet de route", message="Details"
        )
        assignment = ContactAssignment.objects.filter(contact=contact).first()
        assert assignment.assigned_to == user_high

    @patch("apps.core.services.send_notification")
    def test_case_insensitive(self, mock_notify):
        user = UserFactory()
        AssignmentRuleFactory(keywords=["DEVIS"], assigned_user=user)
        contact = Contact.objects.create(
            name="Test", email="t@t.com", subject="demande de devis", message=""
        )
        assert ContactAssignment.objects.filter(contact=contact).exists()

    @patch("apps.core.services.send_notification")
    def test_inactive_rule_skipped(self, mock_notify):
        user = UserFactory()
        AssignmentRuleFactory(keywords=["devis"], assigned_user=user, active=False)
        contact = Contact.objects.create(
            name="Test", email="t@t.com", subject="Demande de devis", message=""
        )
        assert ContactAssignment.objects.filter(contact=contact).count() == 0
