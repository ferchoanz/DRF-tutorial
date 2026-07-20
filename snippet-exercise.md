# Working with Serializers

Before we go any further we'll familiarize ourselves with using our new Serializer class. Let's drop into the Django shell.

```bash
python manage.py shell
```

Okay, once we've got a few imports out of the way, let's create a couple of code snippets to work with.

```bash
>>> from snippets.models import Snippet
>>> from snippets.serializers import SnippetSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser

>>> snippet = Snippet(code='foo = "bar"\n')
>>> snippet.save()

>>> snippet = Snippet(code='print("hello, world")\n')
>>> snippet.save()
```

We've now got a few snippet instances to play with. Let's take a look at serializing one of those instances.

```bash
>>> serializer = SnippetSerializer(snippet)
>>> serializer.data
{'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
```
