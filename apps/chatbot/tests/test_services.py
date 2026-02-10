from unittest.mock import patch

import pytest

from apps.chatbot import services


@pytest.fixture(autouse=True)
def reset_circuit():
    services._failure_count = 0
    services._disabled_until = 0
    yield
    services._failure_count = 0
    services._disabled_until = 0


class TestCircuitBreaker:
    def test_initially_closed(self):
        assert services.is_circuit_open() is False

    def test_opens_after_5_failures(self):
        for _ in range(5):
            services.record_failure()
        assert services.is_circuit_open() is True

    def test_stays_closed_under_5(self):
        for _ in range(4):
            services.record_failure()
        assert services.is_circuit_open() is False

    def test_success_resets_counter(self):
        for _ in range(4):
            services.record_failure()
        services.record_success()
        services.record_failure()
        assert services.is_circuit_open() is False

    @patch("apps.chatbot.services.time")
    def test_closes_after_timeout(self, mock_time):
        mock_time.time.return_value = 1000.0
        for _ in range(5):
            services.record_failure()
        assert services.is_circuit_open() is True
        mock_time.time.return_value = 1301.0
        assert services.is_circuit_open() is False


class TestGetOpenAIClient:
    def setup_method(self):
        services._client = None

    def teardown_method(self):
        services._client = None

    @patch("apps.chatbot.services.OpenAI")
    def test_creates_client_on_first_call(self, mock_openai, settings):
        settings.OPENAI_API_KEY = "test-key"
        client = services.get_openai_client()
        mock_openai.assert_called_once_with(api_key="test-key")
        assert client is mock_openai.return_value

    @patch("apps.chatbot.services.OpenAI")
    def test_reuses_cached_client(self, mock_openai, settings):
        settings.OPENAI_API_KEY = "test-key"
        c1 = services.get_openai_client()
        c2 = services.get_openai_client()
        assert c1 is c2
        mock_openai.assert_called_once()


@pytest.mark.django_db
class TestFetchCompanyStats:
    def test_returns_counts(self):
        from apps.articles.factories import ArticleFactory
        from apps.projects.factories import ProjectFactory

        ProjectFactory.create_batch(3)
        ArticleFactory(published=True)
        stats = services.fetch_company_stats()
        assert stats["project_count"] == 3
        assert stats["article_count"] == 1
        assert isinstance(stats["categories"], dict)
        assert len(stats["categories"]) > 0
