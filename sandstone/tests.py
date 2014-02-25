from concurrency.utils import ConcurrencyTestMixin
from django.test import TestCase

from mezzanine.forms.models import Form
from mezzanine.pages.models import RichTextPage


class RichTextPageLockTestCase(ConcurrencyTestMixin, TestCase):
    concurrency_model = RichTextPage
    concurrency_kwargs = {
        'title': 'test',
        'content': 'Foo',
    }

    def setUp(self):
        self.obj = self.concurrency_model(**self.concurrency_kwargs)
        self.obj.save()


class FormLockTestCase(RichTextPageLockTestCase):
    concurrency_model = Form
