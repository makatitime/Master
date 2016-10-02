from django.conf.urls import patterns, include, url
from django.contrib import admin
from one import views  as one_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'study.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',one_views.index),
    url(r'^add/$',one_views.add,name='add'),
    url(r'^add/(\d+)/(\d+)/$',one_views.add2,name='add2'),
    url(r'^admin/', include(admin.site.urls)),
)
