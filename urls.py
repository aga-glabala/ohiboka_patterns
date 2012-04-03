from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    
    # Examples:
    url(r'^$', 'ohiboka_patterns.bracelet.views.home', name='home'),
    url(r'^login$', 'ohiboka_patterns.bracelet.views.login_user'),
    url(r'^logout$', 'ohiboka_patterns.bracelet.views.logout_user'),
    url(r'^search$', 'ohiboka_patterns.bracelet.views.search'),
    url(r'^comments/(?P<bracelet_id>\d+)/$', 'ohiboka_patterns.comments.views.pattern_comments'),
    url(r'^comments/post/$', 'ohiboka_patterns.comments.views.pattern_comments_post'),
    url(r'^comments/posted/$', 'ohiboka_patterns.comments.views.pattern_comments_posted'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^bracelet/photos/(?P<bracelet_id>\d+)/$', 'ohiboka_patterns.bracelet.views.photos'),
    url(r'^bracelet/photoUpload/(?P<bracelet_id>\d+)', 'ohiboka_patterns.bracelet.views.photo_upload'),
    url(r'^bracelet/(?P<bracelet_id>\d+)/$', 'ohiboka_patterns.bracelet.views.bracelet'),
    url(r'^bracelet/rate/(?P<bracelet_id>\d+)/(?P<bracelet_rate>\d+)/$', 'ohiboka_patterns.bracelet.views.rate'),
    url(r'^add$', 'ohiboka_patterns.bracelet.views.add'),
    url(r'^addpattern$', 'ohiboka_patterns.bracelet.views.addpattern'),
    url(r'^register/$', 'ohiboka_patterns.registration.views.register'),
    #url(r'^login/$', 'ohiboka_patterns.bracelet.views.login_user'),
    # url(r'^ohiboka_patterns/', include('ohiboka_patterns.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lang/(?P<lang>\w+)', 'ohiboka_patterns.bracelet.views.setlang'),
)

urlpatterns += staticfiles_urlpatterns()
