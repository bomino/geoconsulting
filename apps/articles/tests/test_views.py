import pytest
from django.test import Client
from django.utils import timezone

from apps.articles.factories import ArticleFactory


@pytest.mark.django_db
class TestArticleViews:
    def setup_method(self):
        self.client = Client()

    def test_list_200(self):
        ArticleFactory(published=True)
        response = self.client.get("/actualites/")
        assert response.status_code == 200

    def test_detail_published(self):
        a = ArticleFactory(published=True, slug="test-article")
        response = self.client.get(f"/actualites/{a.slug}/")
        assert response.status_code == 200

    def test_detail_unpublished_404(self):
        a = ArticleFactory(published=False, slug="hidden-article")
        response = self.client.get(f"/actualites/{a.slug}/")
        assert response.status_code == 404
