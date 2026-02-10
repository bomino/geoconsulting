from unittest.mock import patch

import pytest
from django.test import Client

from apps.contacts.models import Contact

CONTACT_URL = "/contact/"
VALID_POST = {
    "name": "Moussa Ibrahim",
    "email": "moussa@example.com",
    "phone": "+227 90 00 00 00",
    "subject": "Devis",
    "message": "Bonjour, je souhaite un devis.",
    "company_fax": "",
}


@pytest.mark.django_db
class TestContactView:
    def setup_method(self):
        self.client = Client()

    def test_get_renders_form(self):
        response = self.client.get(CONTACT_URL)
        assert response.status_code == 200
        assert b"name" in response.content

    @patch("apps.core.services.send_notification")
    @patch("apps.crm.services.auto_assign_contact")
    def test_post_valid_creates_contact(self, mock_assign, mock_notify):
        response = self.client.post(CONTACT_URL, VALID_POST)
        assert response.status_code == 302
        assert Contact.objects.filter(email="moussa@example.com").exists()

    @patch("apps.core.services.send_notification")
    @patch("apps.crm.services.auto_assign_contact")
    def test_post_honeypot_discards(self, mock_assign, mock_notify):
        data = {**VALID_POST, "company_fax": "bot"}
        response = self.client.post(CONTACT_URL, data)
        assert response.status_code == 302
        assert Contact.objects.count() == 0

    @patch("apps.core.services.send_notification")
    @patch("apps.crm.services.auto_assign_contact")
    def test_post_htmx_returns_partial(self, mock_assign, mock_notify):
        response = self.client.post(
            CONTACT_URL, VALID_POST, HTTP_HX_REQUEST="true"
        )
        assert response.status_code == 200

    def test_post_invalid_rerenders(self):
        data = {**VALID_POST, "email": ""}
        response = self.client.post(CONTACT_URL, data)
        assert response.status_code == 200
        assert Contact.objects.count() == 0
