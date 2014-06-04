from django.conf.urls import patterns, url

from protected_assets import views


urlpatterns = patterns('',
    url(r'^download-agreement/$', views.sign_agreement, name='protected_assets.sign_agreement'),
    url(r'^admin/protected_assets/signedagreement/csv/$', views.export_signedagreement_csv,
        name='protected_assets.export_signedagreement_csv'),
)
