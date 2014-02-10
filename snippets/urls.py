from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^templates/$', 'snippets.views.snippet_templates'),
    url(r'^detail/(?P<snippet_id>\d+)/$', 'snippets.views.snippet_detail', name='snippet-content'),
)