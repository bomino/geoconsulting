import pytest
from django.test import RequestFactory

from apps.audit.middleware import AuditMiddleware
from apps.audit.services import get_request_metadata


@pytest.mark.django_db
class TestAuditMiddleware:
    def setup_method(self):
        self.rf = RequestFactory()
        self.middleware = AuditMiddleware(lambda req: req)

    def test_extracts_remote_addr(self):
        request = self.rf.get("/", REMOTE_ADDR="192.168.1.1")
        self.middleware(request)
        meta = get_request_metadata()
        assert meta["ip_address"] == "192.168.1.1"

    def test_extracts_xff_single(self):
        request = self.rf.get("/", HTTP_X_FORWARDED_FOR="1.2.3.4")
        self.middleware(request)
        meta = get_request_metadata()
        assert meta["ip_address"] == "1.2.3.4"

    def test_extracts_xff_multiple(self):
        request = self.rf.get("/", HTTP_X_FORWARDED_FOR="1.2.3.4, 5.6.7.8")
        self.middleware(request)
        meta = get_request_metadata()
        assert meta["ip_address"] == "1.2.3.4"

    def test_extracts_user_agent(self):
        request = self.rf.get("/", HTTP_USER_AGENT="TestBot/1.0")
        self.middleware(request)
        meta = get_request_metadata()
        assert meta["user_agent"] == "TestBot/1.0"
