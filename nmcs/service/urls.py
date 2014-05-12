from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(
        r'^create/(?P<pk>\d+)$',
        views.ServiceCreateView.as_view(),
        name='service-create'
    ),
    url(
        r'^update/(?P<pk>\d+)$',
        views.ServiceUpdateView.as_view(),
        name='service-update'
    ),
    url(
        r'^detail/(?P<pk>\d+)$',
        views.ServiceDetailView.as_view(),
        name='service-detail'
    ),
    url(
        r'^delete/(?P<pk>\d+)$',
        views.ServiceDeleteView.as_view(),
        name='service-delete'
    ),

)