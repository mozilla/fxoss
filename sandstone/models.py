from mezzanine.forms.models import Form
from mezzanine.pages.models import RichTextPage

from concurrency.api import apply_concurrency_check
from concurrency.fields import IntegerVersionField


apply_concurrency_check(Form, 'version', IntegerVersionField)
apply_concurrency_check(RichTextPage, 'version', IntegerVersionField)
