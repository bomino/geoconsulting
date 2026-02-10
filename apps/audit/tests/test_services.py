import pytest

from apps.accounts.factories import UserFactory
from apps.audit.models import AuditLog
from apps.audit.services import get_request_metadata, log_audit_event, set_request_metadata


@pytest.mark.django_db
class TestLogAuditEvent:
    def test_creates_record(self):
        user = UserFactory()
        log_audit_event(user=user, action="created", entity_type="Project", entity_id="1")
        log = AuditLog.objects.filter(entity_type="Project").first()
        assert log is not None
        assert log.user == user
        assert log.action == "created"
        assert log.entity_id == "1"

    def test_nullable_user(self):
        log_audit_event(user=None, action="deleted", entity_type="Contact", entity_id="5")
        log = AuditLog.objects.filter(entity_type="Contact").first()
        assert log is not None
        assert log.user is None


class TestRequestMetadata:
    def test_set_and_get(self):
        set_request_metadata("10.0.0.1", "Mozilla/5.0")
        meta = get_request_metadata()
        assert meta["ip_address"] == "10.0.0.1"
        assert meta["user_agent"] == "Mozilla/5.0"

    @pytest.mark.django_db
    def test_audit_event_includes_metadata(self):
        set_request_metadata("203.0.113.1", "TestClient/2.0")
        user = UserFactory()
        log_audit_event(user=user, action="updated", entity_type="Article", entity_id="7")
        log = AuditLog.objects.filter(entity_type="Article").first()
        assert log.ip_address == "203.0.113.1"
        assert log.user_agent == "TestClient/2.0"
