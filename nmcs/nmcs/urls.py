from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nmcs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('customers.urls')),
    url(r'^service/', include('service.urls')),
    url(r'^work/', include('work.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
