from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'project.app.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'project.app.views.signup_email'),
    url(r'^email-sent/', 'project.app.views.validation_sent'),
    url(r'^login/$', 'project.app.views.home'),
    url(r'^done/$', 'project.app.views.done', name='done'),
    url(r'^email/$', 'project.app.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)
