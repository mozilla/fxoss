from django.db import models

from mezzanine.core.fields import RichTextField


class TinyMCESnippet(models.Model):
    """Stores small snippets for common content patterns."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    content = RichTextField()
    notes = models.TextField(verbose_name='description', default='', blank=True)

