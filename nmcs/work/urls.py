from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    # url(
    #     r'^create/(?P<pk>\d+)$',
    #     views.WorkCreateView.as_view(),
    #     name='work-create'
    # ),
    url(
        r'^create/(?P<pk>\d+)$',
        views.workCreateView,
        name='work-create'
    ),
    url(
        r'^create/(?P<pk>\d+)/(?P<workorder>\d+)$',
        views.workCreateView,
        name='work-create'
    ),
    url(
        r'^pdf/$',
        views.some_view3,
        name='work-pdf'
    ),

)