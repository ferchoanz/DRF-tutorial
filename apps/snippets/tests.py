from django.test import TestCase

from apps.snippets.models import Snippet
from apps.snippets.serializers import SnippetSerializer, SnippetModelSerializer


class SnippetModelTests(TestCase):
    def test_create_snippet(self):
        snippet = Snippet.objects.create(
            title="Test Snippet",
            code='print("hello world")',
            language="python",
            style="friendly",
        )
        self.assertEqual(snippet.title, "Test Snippet")
        self.assertEqual(snippet.language, "python")
        self.assertTrue(snippet.created)

    def test_default_language_and_style(self):
        snippet = Snippet.objects.create(code="x = 1")
        self.assertEqual(snippet.language, "python")
        self.assertEqual(snippet.style, "friendly")
        self.assertFalse(snippet.linenos)

    def test_ordering_by_created(self):
        first = Snippet.objects.create(code="first")
        second = Snippet.objects.create(code="second")
        snippets = list(Snippet.objects.all())
        self.assertEqual(snippets, [first, second])


class SnippetSerializerTests(TestCase):
    def test_serialize_snippet(self):
        snippet = Snippet.objects.create(
            title="Hello",
            code='print("hello")',
            language="python",
            style="friendly",
        )
        serializer = SnippetSerializer(snippet)
        self.assertEqual(serializer.data["title"], "Hello")
        self.assertEqual(serializer.data["code"], 'print("hello")')
        self.assertEqual(serializer.data["language"], "python")

    def test_create_with_serializer(self):
        payload = {
            "title": "New Snippet",
            "code": "x = 42",
            "linenos": True,
            "language": "python",
            "style": "friendly",
        }
        serializer = SnippetSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        snippet = serializer.save()
        self.assertEqual(snippet.title, payload["title"])
        self.assertEqual(snippet.code, payload["code"])
        self.assertTrue(snippet.linenos)

    def test_update_with_serializer(self):
        snippet = Snippet.objects.create(
            title="Old",
            code="old code",
            language="python",
            style="friendly",
        )
        payload = {
            "title": "Updated",
            "code": "updated code",
            "linenos": False,
            "language": "python",
            "style": "friendly",
        }
        serializer = SnippetSerializer(snippet, data=payload)
        self.assertTrue(serializer.is_valid())
        updated = serializer.save()
        self.assertEqual(updated.title, "Updated")
        self.assertEqual(updated.code, "updated code")

    def test_invalid_language_choice(self):
        payload = {
            "title": "Bad Language",
            "code": "x = 1",
            "language": "not-a-language",
            "style": "friendly",
        }
        serializer = SnippetSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("language", serializer.errors)

    def test_invalid_style_choice(self):
        payload = {
            "title": "Bad Style",
            "code": "x = 1",
            "language": "python",
            "style": "not-a-style",
        }
        serializer = SnippetSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("style", serializer.errors)

    def test_model_serializer_fields(self):
        snippet = Snippet.objects.create(
            title="Model Serializer Test",
            code="x = 1",
            language="python",
            style="friendly",
        )
        serializer = SnippetModelSerializer(snippet)
        expected_fields = {"id", "title", "code", "linenos", "language", "style"}
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_model_serializer_create(self):
        payload = {
            "title": "Created via ModelSerializer",
            "code": "y = 2",
            "linenos": True,
            "language": "python",
            "style": "friendly",
        }
        serializer = SnippetModelSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        snippet = serializer.save()
        self.assertEqual(snippet.title, payload["title"])
