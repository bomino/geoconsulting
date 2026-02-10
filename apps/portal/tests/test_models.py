import pytest
from django.db import IntegrityError

from apps.portal.factories import ClientProjectFactory, MessageFactory
from apps.portal.models import ClientProject, Message


@pytest.mark.django_db
class TestClientProject:
    def test_unique_together(self):
        cp = ClientProjectFactory()
        with pytest.raises(IntegrityError):
            ClientProjectFactory(user=cp.user, project=cp.project)

    def test_str(self):
        cp = ClientProjectFactory()
        result = str(cp)
        assert cp.user.username in result
        assert cp.project.title in result

    def test_message_ordering(self):
        m1 = MessageFactory()
        m2 = MessageFactory()
        result = list(Message.objects.all())
        assert result[0] == m2
