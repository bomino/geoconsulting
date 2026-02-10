import pytest

from apps.audit.models import AuditLog


@pytest.mark.django_db
class TestAuditLog:
    def test_ordering_newest_first(self):
        AuditLog.objects.create(action="a", entity_type="X", entity_id="1")
        AuditLog.objects.create(action="b", entity_type="X", entity_id="2")
        result = list(AuditLog.objects.all())
        assert result[0].action == "b"

    def test_nullable_user(self):
        log = AuditLog.objects.create(
            user=None, action="test", entity_type="Test", entity_id="0"
        )
        assert log.user is None
        assert log.pk is not None
