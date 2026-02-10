import json
from unittest.mock import MagicMock, patch

import pytest
from django.test import Client

CHATBOT_URL = "/api/chatbot/"


@pytest.fixture(autouse=True)
def reset_circuit():
    from apps.chatbot import services
    services._failure_count = 0
    services._disabled_until = 0
    yield
    services._failure_count = 0
    services._disabled_until = 0


@pytest.mark.django_db
class TestChatbotView:
    def setup_method(self):
        self.client = Client()

    @patch("apps.chatbot.views.get_openai_client")
    @patch("apps.chatbot.views.is_circuit_open", return_value=False)
    def test_valid_post_returns_sse(self, mock_circuit, mock_client):
        mock_stream = MagicMock()
        mock_choice = MagicMock()
        mock_choice.delta.content = "Bonjour"
        mock_chunk = MagicMock()
        mock_chunk.choices = [mock_choice]
        mock_stream.__iter__ = MagicMock(return_value=iter([mock_chunk]))
        mock_client.return_value.chat.completions.create.return_value = mock_stream

        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Bonjour"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response["Content-Type"] == "text/event-stream"

    def test_empty_message_400(self):
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": ""}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_message_too_long_400(self):
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "x" * 2001}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_invalid_json_400(self):
        response = self.client.post(
            CHATBOT_URL,
            "not json",
            content_type="application/json",
        )
        assert response.status_code == 400

    @patch("apps.chatbot.views.is_circuit_open", return_value=True)
    def test_circuit_open_503(self, mock_circuit):
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Test"}),
            content_type="application/json",
        )
        assert response.status_code == 503

    def test_get_not_allowed(self):
        response = self.client.get(CHATBOT_URL)
        assert response.status_code == 405

    @patch("apps.chatbot.views.get_openai_client")
    @patch("apps.chatbot.views.is_circuit_open", return_value=False)
    def test_openai_error_502(self, mock_circuit, mock_client):
        mock_client.return_value.chat.completions.create.side_effect = Exception("API error")
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Test"}),
            content_type="application/json",
        )
        assert response.status_code == 502

    @patch("apps.chatbot.views.get_openai_client")
    @patch("apps.chatbot.views.is_circuit_open", return_value=False)
    def test_history_non_list_ignored(self, mock_circuit, mock_client):
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(return_value=iter([]))
        mock_client.return_value.chat.completions.create.return_value = mock_stream
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Test", "history": "not-a-list"}),
            content_type="application/json",
        )
        assert response.status_code == 200

    @patch("apps.chatbot.views.get_openai_client")
    @patch("apps.chatbot.views.is_circuit_open", return_value=False)
    def test_history_entries_forwarded(self, mock_circuit, mock_client):
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(return_value=iter([]))
        mock_client.return_value.chat.completions.create.return_value = mock_stream
        history = [
            {"role": "user", "content": "Bonjour"},
            {"role": "assistant", "content": "Salut"},
            {"role": "invalid", "content": "skip"},
        ]
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Suite", "history": history}),
            content_type="application/json",
        )
        assert response.status_code == 200
        call_args = mock_client.return_value.chat.completions.create.call_args
        messages = call_args[1]["messages"]
        roles = [m["role"] for m in messages]
        assert roles.count("user") == 2
        assert roles.count("assistant") == 1

    @patch("apps.chatbot.views.get_openai_client")
    @patch("apps.chatbot.views.is_circuit_open", return_value=False)
    def test_streaming_body_content(self, mock_circuit, mock_client):
        mock_choice = MagicMock()
        mock_choice.delta.content = "Bonjour"
        mock_chunk = MagicMock()
        mock_chunk.choices = [mock_choice]
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(return_value=iter([mock_chunk]))
        mock_client.return_value.chat.completions.create.return_value = mock_stream
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Test"}),
            content_type="application/json",
        )
        content = b"".join(response.streaming_content).decode()
        assert "Bonjour" in content
        assert "[DONE]" in content

    @patch("apps.chatbot.views.get_openai_client")
    @patch("apps.chatbot.views.is_circuit_open", return_value=False)
    def test_streaming_error_yields_error_event(self, mock_circuit, mock_client):
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(side_effect=Exception("stream fail"))
        mock_client.return_value.chat.completions.create.return_value = mock_stream
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Test"}),
            content_type="application/json",
        )
        content = b"".join(response.streaming_content).decode()
        assert "error" in content

    @patch("apps.chatbot.views.get_openai_client")
    @patch("apps.chatbot.views.is_circuit_open", return_value=False)
    def test_chunk_with_no_choices_skipped(self, mock_circuit, mock_client):
        mock_chunk_empty = MagicMock()
        mock_chunk_empty.choices = []
        mock_choice = MagicMock()
        mock_choice.delta.content = "OK"
        mock_chunk_valid = MagicMock()
        mock_chunk_valid.choices = [mock_choice]
        mock_stream = MagicMock()
        mock_stream.__iter__ = MagicMock(return_value=iter([mock_chunk_empty, mock_chunk_valid]))
        mock_client.return_value.chat.completions.create.return_value = mock_stream
        response = self.client.post(
            CHATBOT_URL,
            json.dumps({"message": "Test"}),
            content_type="application/json",
        )
        content = b"".join(response.streaming_content).decode()
        assert "OK" in content
