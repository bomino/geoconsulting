from unittest.mock import patch

import pytest

from apps.contacts.factories import ContactFactory


@pytest.mark.django_db
class TestContactSignals:
    @patch("apps.crm.services.auto_assign_contact")
    @patch("apps.core.services.send_notification")
    def test_created_triggers_auto_assign(self, mock_notify, mock_assign):
        ContactFactory()
        mock_assign.assert_called_once()

    @patch("apps.crm.services.auto_assign_contact")
    @patch("apps.core.services.send_notification")
    def test_created_triggers_notification(self, mock_notify, mock_assign):
        ContactFactory()
        mock_notify.assert_called_once()

    @patch("apps.crm.services.auto_assign_contact")
    @patch("apps.core.services.send_notification")
    def test_update_does_not_trigger(self, mock_notify, mock_assign):
        contact = ContactFactory()
        mock_assign.reset_mock()
        mock_notify.reset_mock()
        contact.notes = "Updated"
        contact.save()
        mock_assign.assert_not_called()
        mock_notify.assert_not_called()
