import time

from django.conf import settings
from openai import OpenAI

_client = None
_failure_count = 0
_disabled_until = 0


def get_openai_client():
    global _client
    if _client is None:
        api_key = getattr(settings, "OPENAI_API_KEY", "")
        _client = OpenAI(api_key=api_key)
    return _client


def is_circuit_open():
    return time.time() < _disabled_until


def record_failure():
    global _failure_count, _disabled_until
    _failure_count += 1
    if _failure_count >= 5:
        _disabled_until = time.time() + 300


def record_success():
    global _failure_count
    _failure_count = 0


def fetch_company_stats():
    from apps.articles.models import Article
    from apps.core.enums import ProjectCategory
    from apps.projects.models import Project

    stats = {
        "project_count": int(Project.objects.filter(published=True).count()),
        "article_count": int(Article.objects.filter(published=True).count()),
        "categories": {},
    }
    for cat in ProjectCategory:
        stats["categories"][cat.label] = int(
            Project.objects.filter(published=True, category=cat.value).count()
        )
    return stats
