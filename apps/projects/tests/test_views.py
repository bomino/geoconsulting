import pytest
from django.test import Client

from apps.projects.factories import ProjectFactory


@pytest.mark.django_db
class TestProjectViews:
    def setup_method(self):
        self.client = Client()

    def test_list_200(self):
        ProjectFactory()
        response = self.client.get("/projets/")
        assert response.status_code == 200

    def test_detail_published(self):
        p = ProjectFactory(published=True, slug="test-proj")
        response = self.client.get(f"/projets/{p.slug}/")
        assert response.status_code == 200

    def test_detail_unpublished_404(self):
        p = ProjectFactory(published=False, slug="hidden-proj")
        response = self.client.get(f"/projets/{p.slug}/")
        assert response.status_code == 404

    def test_list_htmx_partial(self):
        ProjectFactory()
        response = self.client.get("/projets/", HTTP_HX_REQUEST="true")
        assert response.status_code == 200
