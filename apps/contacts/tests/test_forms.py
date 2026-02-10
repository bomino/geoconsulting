import pytest

from apps.contacts.forms import ContactForm

VALID_DATA = {
    "name": "Moussa Ibrahim",
    "email": "moussa@example.com",
    "phone": "+227 90 00 00 00",
    "subject": "Demande de devis",
    "message": "Bonjour, je souhaite un devis.",
    "company_fax": "",
}


class TestContactForm:
    def test_valid_form(self):
        form = ContactForm(data=VALID_DATA)
        assert form.is_valid()

    def test_missing_name(self):
        data = {**VALID_DATA, "name": ""}
        assert not ContactForm(data=data).is_valid()

    def test_missing_email(self):
        data = {**VALID_DATA, "email": ""}
        assert not ContactForm(data=data).is_valid()

    def test_missing_message(self):
        data = {**VALID_DATA, "message": ""}
        assert not ContactForm(data=data).is_valid()

    def test_honeypot_empty_returns_false(self):
        form = ContactForm(data=VALID_DATA)
        form.is_valid()
        assert form.is_honeypot_filled() is False

    def test_honeypot_filled_returns_true(self):
        data = {**VALID_DATA, "company_fax": "spam bot fill"}
        form = ContactForm(data=data)
        form.is_valid()
        assert form.is_honeypot_filled() is True
