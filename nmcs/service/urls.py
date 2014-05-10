from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(
        r'^create/(?P<pk>\d+)$',
        views.ServiceCreateView.as_view(),
        name='service-create'
    ),



)