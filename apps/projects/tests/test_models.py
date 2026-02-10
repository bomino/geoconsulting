import pytest
from django.db import IntegrityError

from apps.projects.factories import ProjectDocumentFactory, ProjectFactory
from apps.projects.models import Project


@pytest.mark.django_db
class TestProject:
    def test_str(self):
        p = ProjectFactory(title="Pont Niamey")
        assert str(p) == "Pont Niamey"

    def test_get_absolute_url(self):
        p = ProjectFactory(slug="pont-niamey")
        assert p.get_absolute_url() == "/projets/pont-niamey/"

    def test_slug_unique(self):
        ProjectFactory(slug="unique-slug")
        with pytest.raises(IntegrityError):
            ProjectFactory(slug="unique-slug")


@pytest.mark.django_db
class TestProjectDocument:
    def test_str(self):
        doc = ProjectDocumentFactory(title="Rapport final")
        assert f"Rapport final ({doc.project.title})" == str(doc)

    def test_size_display_bytes(self):
        doc = ProjectDocumentFactory()
        with pytest.MonkeyPatch.context() as m:
            m.setattr(type(doc.file), "size", property(lambda self: 512))
            assert doc.size_display == "512.0 B"

    def test_size_display_kb(self):
        doc = ProjectDocumentFactory()
        with pytest.MonkeyPatch.context() as m:
            m.setattr(type(doc.file), "size", property(lambda self: 2048))
            assert doc.size_display == "2.0 KB"

    def test_size_display_mb(self):
        doc = ProjectDocumentFactory()
        with pytest.MonkeyPatch.context() as m:
            m.setattr(type(doc.file), "size", property(lambda self: 5 * 1024 * 1024))
            assert doc.size_display == "5.0 MB"
