from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

from .models import TinyMCESnippet


@staff_member_required
def snippet_templates(request):
    """View for listing available TinyMCE templates.
    See http://www.tinymce.com/wiki.php/Plugin3x:template for the expected format
    of this response.
    """
    snippets = TinyMCESnippet.objects.all().order_by('title')
    return render(request, 'snippets/snippets.js', {'snippets': snippets}, content_type='application/javascript')


@staff_member_required
def snippet_detail(request, snippet_id):
    """Detail view for TinyMCE to get the content of a given snippet.
    See http://www.tinymce.com/wiki.php/Plugin3x:template for the expected format
    of this response.
    """
    snippet = get_object_or_404(TinyMCESnippet, pk=snippet_id)
    return render(request, 'snippets/snippet.html', {'snippet': snippet})
