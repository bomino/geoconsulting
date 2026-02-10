import pytest

from apps.audit.models import AuditLog
from apps.audit.signals import _get_user
from apps.projects.factories import ProjectFactory


@pytest.mark.django_db
class TestAuditSignals:
    def test_log_on_project_create(self):
        initial_count = AuditLog.objects.count()
        ProjectFactory()
        assert AuditLog.objects.count() > initial_count
        log = AuditLog.objects.filter(entity_type="Project", action="created").first()
        assert log is not None

    def test_log_on_project_update(self):
        p = ProjectFactory()
        initial_count = AuditLog.objects.count()
        p.title = "Updated"
        p.save()
        new_log = AuditLog.objects.filter(entity_type="Project", action="updated").first()
        assert new_log is not None

    def test_log_on_project_delete(self):
        p = ProjectFactory()
        pk = p.pk
        p.delete()
        log = AuditLog.objects.filter(entity_type="Project", action="deleted").first()
        assert log is not None
        assert log.entity_id == str(pk)

    def test_get_user_extracts_created_by(self):
        p = ProjectFactory()
        assert _get_user(p) == p.created_by

    def test_get_user_returns_none_for_no_attrs(self):
        class Dummy:
            pass
        assert _get_user(Dummy()) is None
