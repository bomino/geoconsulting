import factory

from apps.accounts.factories import UserFactory
from apps.core.enums import AccessLevel
from apps.portal.models import ClientProject, Message
from apps.projects.factories import ProjectFactory


class ClientProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientProject

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    access_level = AccessLevel.VIEW


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
    subject = factory.Sequence(lambda n: f"Message {n}")
    content = "Contenu du message de test."
