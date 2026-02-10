import factory

from apps.accounts.factories import UserFactory
from apps.contacts.models import Contact, ContactAssignment


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker("name")
    email = factory.Faker("email")
    phone = "+227 90 00 00 00"
    subject = factory.Sequence(lambda n: f"Demande {n}")
    message = "Message de test pour le formulaire de contact."


class ContactAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactAssignment

    contact = factory.SubFactory(ContactFactory)
    assigned_to = factory.SubFactory(UserFactory)
