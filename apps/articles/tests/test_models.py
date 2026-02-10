import pytest
from django.db import IntegrityError
from django.utils import timezone

from apps.articles.factories import ArticleFactory


@pytest.mark.django_db
class TestArticle:
    def test_auto_published_at_on_publish(self):
        article = ArticleFactory(published=True)
        assert article.published_at is not None

    def test_unpublish_clears_date(self):
        article = ArticleFactory(published=True)
        article.published = False
        article.save()
        article.refresh_from_db()
        assert article.published_at is None

    def test_published_at_not_overwritten(self):
        fixed_date = timezone.now().replace(year=2020)
        article = ArticleFactory(published=True, published_at=fixed_date)
        article.title = "Updated"
        article.save()
        article.refresh_from_db()
        assert article.published_at == fixed_date

    def test_slug_unique(self):
        ArticleFactory(slug="unique-article")
        with pytest.raises(IntegrityError):
            ArticleFactory(slug="unique-article")
