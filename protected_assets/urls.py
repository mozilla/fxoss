from django.conf.urls import patterns, url

from protected_assets import views


urlpatterns = patterns('',
    url(r'^download-agreement/$', views.sign_agreement, name='protected_assets.sign_agreement'),
)
