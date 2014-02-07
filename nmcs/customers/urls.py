from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(
        r'^(?P<pk>\d+)$',
        views.CustomerView.as_view(), 
        name='customer-detail'

    ),
    url(
        r"^$",
        views.CustomerListView.as_view(),
        name='customer-list'

    ),
    url(
        r"^add",
        views.addView,
        name='customer-add'

    ),
    url(
        r"^delete/(?P<pk>\d+)$",
        views.CustomerDeleteView.as_view(),
        name='customer-delete'

    ),
    url(
        r"^update/(?P<pk>\d+)$",
        views.CustomerUpdateView.as_view(),
        name='customer-update'

    ),


)