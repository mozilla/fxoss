from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^templates/$', 'snippets.views.snippet_templates'),
)