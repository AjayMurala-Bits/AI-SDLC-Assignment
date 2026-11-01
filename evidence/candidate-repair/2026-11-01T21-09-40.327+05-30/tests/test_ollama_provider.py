import unittest

from movie_review_summarizer.provider import OllamaProvider, ProviderConfig
from movie_review_summarizer.schema import success_schema


class _Completions:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        usage = type("Usage", (), {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2})()
        message = type("Message", (), {"content": '{"summary":"A review.","sentiment":"negative","positive_aspects":[],"negative_aspects":["Slow pacing"],"recommendation":"Consider cautiously."}'})()
        choice = type("Choice", (), {"message": message})()
        return type("Response", (), {"choices": [choice], "usage": usage})()


class _Client:
    def __init__(self):
        self.completions = _Completions()
        self.chat = type("Chat", (), {"completions": self.completions})()


class OllamaProviderTests(unittest.TestCase):
    def test_summary_uses_existing_schema_in_ollama_request(self):
        config = ProviderConfig(api_key="", model="llama3.2:latest", provider="ollama", base_url="http://127.0.0.1:11434/v1")
        provider = OllamaProvider(config, "summarize", "judge")
        client = _Client()
        provider._client = client
        result = provider.summarize("The pacing is slow.")
        request_schema = client.completions.kwargs["response_format"]["json_schema"]["schema"]
        self.assertEqual(request_schema, success_schema())
        self.assertEqual(client.completions.kwargs["response_format"]["type"], "json_schema")
        self.assertEqual(result["sentiment"], "negative")

