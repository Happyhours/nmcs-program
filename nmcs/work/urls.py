from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(
        r'^pdf/$',
        views.some_view3,
        name='work-pdf'
    ),

)