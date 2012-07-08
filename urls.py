from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    url(r'^$', 'ohibokapatterns.bracelet.views.home', name = 'home'),
    url(r'^login$', 'ohibokapatterns.bracelet.views.login_user'),
    url(r'^logout$', 'ohibokapatterns.bracelet.views.logout_user'),
    url(r'^facebook_login/$', 'ohibokapatterns.bracelet.views.facebook_login'),
    url(r'^facebook_login_success/$', 'ohibokapatterns.bracelet.views.facebook_login_success'),
    url(r'^search$', 'ohibokapatterns.bracelet.views.search'),
    url(r'^comments/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.comments.views.pattern_comments'),
    url(r'^comments/post/$', 'ohibokapatterns.comments.views.pattern_comments_post'),
    url(r'^comments/posted/$', 'ohibokapatterns.comments.views.pattern_comments_posted'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^bracelet/photos/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.bracelet.views.photos'),
    url(r'^bracelet/photoUpload/(?P<bracelet_id>\d+)', 'ohibokapatterns.bracelet.views.photo_upload'),
    url(r'^bracelet/photo/remove/(?P<photo_id>\d+)', 'ohibokapatterns.registration.views.delete_photo'),
    url(r'^bracelet/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.bracelet.views.bracelet'),
    url(r'^bracelet/remove/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.registration.views.delete_bracelet'),
    url(r'^bracelet/rate/(?P<bracelet_id>\d+)/(?P<bracelet_rate>\d+)/$', 'ohibokapatterns.bracelet.views.rate'),
    url(r'^bracelet/rate/remove/(?P<rate_id>\d+)', 'ohibokapatterns.registration.views.delete_rate'),
    url(r'^add$', 'ohibokapatterns.bracelet.views.add'),
    url(r'^addpattern$', 'ohibokapatterns.bracelet.views.addpattern'),
    url(r'^register/$', 'ohibokapatterns.registration.views.register'),
    url(r'^profile/$', 'ohibokapatterns.registration.views.userprofile'),
    url(r'^user/(?P<user_id>\d+)', 'ohibokapatterns.registration.views.user'),
    url(r'^about/$', 'ohibokapatterns.registration.views.about'),
    url(r'^privacypolicy/$', 'ohibokapatterns.registration.views.privacypolicy'),
    #url(r'^login/$', 'ohibokapatterns.bracelet.views.login_user'),
    # url(r'^ohibokapatterns/', include('ohibokapatterns.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:  
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lang/(?P<lang>\w+)', 'ohibokapatterns.bracelet.views.setlang'),
)

urlpatterns += staticfiles_urlpatterns()
