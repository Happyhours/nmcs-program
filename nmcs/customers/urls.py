from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(
        r'^(?P<pk>\d+)$',
        views.CustomerDetailView.as_view(), 
        name='customer-detail'

    ),
    url(
        r"^$",
        views.CustomerListView.as_view(),
        name='customer-list'

    ),
    url(
        r"^add$",
        views.addView,
        name='customer-add'

    ),



)