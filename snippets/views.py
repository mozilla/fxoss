from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def snippet_templates(request):
    """View for listing available TinyMCE templates.
    See http://www.tinymce.com/wiki.php/Plugin3x:template for the expected format
    of this response.
    """
    templates = []
    return render(request, 'snippets/snippets.js', {'templates': templates}, content_type='application/javascript')
