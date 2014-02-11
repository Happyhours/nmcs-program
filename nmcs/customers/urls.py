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
    url(
        r'^update/mc/(?P<pk>\w+)$',
        views.McUpdateView.as_view(),
        name='mc-update'
    ),
    url(
        r'^delete/mc/(?P<pk>\w+)$',
        views.McDeleteView.as_view(),
        name='mc-delete'
    ),
    url(
        r'^customer/create/(?P<pk>\w+)$',
        views.McCreateView.as_view(),
        name='mc-create'
    )


)