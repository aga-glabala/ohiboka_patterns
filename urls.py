from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',

    # MODULE COMMON
    url(r'^$', 'ohibokapatterns.common.views.index', name = 'home'),
    url(r'^login$', 'ohibokapatterns.common.views.login_user'),
    url(r'^logout$', 'ohibokapatterns.common.views.logout_user'),
    url(r'^facebook_login/$', 'ohibokapatterns.common.views.facebook_login'),
    url(r'^facebook_login_success/$', 'ohibokapatterns.common.views.facebook_login_success'),
    url(r'^search$', 'ohibokapatterns.common.views.search'),
    url(r'^register/$', 'ohibokapatterns.common.views.register'),
    url(r'^profile/$', 'ohibokapatterns.common.views.userprofile'),
    url(r'^user/(?P<user_name>.*)', 'ohibokapatterns.common.views.user'),
    url(r'^about/$', 'ohibokapatterns.common.views.about'),
    url(r'^privacypolicy/$', 'ohibokapatterns.common.views.privacypolicy'),
    url(r'^lang/(?P<lang>\w+)', 'ohibokapatterns.common.views.setlang'),
    url(r'^contact/success/$', 'ohibokapatterns.common.views.contact_success'),

    # MODULE BRACELET
    url(r'^bracelet/photos/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.bracelet.views.photos'),
    url(r'^bracelet/photoUpload/(?P<bracelet_id>\d+)', 'ohibokapatterns.bracelet.views.photo_upload'),
    url(r'^bracelet/photo/remove/(?P<photo_id>\d+)', 'ohibokapatterns.bracelet.views.delete_photo'),
    url(r'^bracelet/remove/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.bracelet.views.delete_bracelet'),
    url(r'^bracelet/rate/(?P<bracelet_id>\d+)/(?P<bracelet_rate>\d+)/$', 'ohibokapatterns.bracelet.views.rate'),
    url(r'^bracelet/rate/remove/(?P<rate_id>\d+)', 'ohibokapatterns.bracelet.views.delete_rate'),
    url(r'^bracelet/change_status/(?P<bracelet_id>\d+)$', 'ohibokapatterns.bracelet.views.change_status'),
    url(r'^bracelet/delete/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.bracelet.views.delete_bracelet'),
    # TODO minus przy statusie!
    url(r'^bracelet/accept/(?P<bracelet_id>\d+)/(?P<bracelet_status>\d+)/$', 'ohibokapatterns.bracelet.views.accept'),
    url(r'^add$', 'ohibokapatterns.bracelet.views.add'),
    url(r'^addpattern$', 'ohibokapatterns.bracelet.views.addpattern'),
    url(r'^bracelet/(?P<bracelet_url>.+)/$', 'ohibokapatterns.bracelet.views.bracelet'),

    # MODULE COMMENT
    url(r'^comments/(?P<bracelet_id>\d+)/$', 'ohibokapatterns.comments.views.pattern_comments'),
    url(r'^comments/post/$', 'ohibokapatterns.comments.views.pattern_comments_post'),
    url(r'^comments/posted/$', 'ohibokapatterns.comments.views.pattern_comments_posted'),
    url(r'^comments/', include('django.contrib.comments.urls')),

    # MODULE ADMIN
    url(r'admin/manage_bracelets', 'ohibokapatterns.admin.views.manage_bracelets'),

    # Uncomment the admin/doc line below to enable admin documentation:  
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^password_change/$', 'django.contrib.auth.views.password_change', name = 'password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name = 'password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name = 'password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name = 'password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name = 'password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name = 'password_reset_complete'),

    # Uncomment the next line to enable the admin:
    url(r'^superadmin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
