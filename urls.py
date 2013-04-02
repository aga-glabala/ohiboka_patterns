from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',

                       # MODULE COMMON
                       url(r'^$', 'common.views.index', name='home'),
                       url(r'^login/?$', 'common.views.login_user'),
                       url(r'^logout/?$', 'common.views.logout_user'),
                       url(r'^facebook_login/?$',
                           'common.views.facebook_login'),
                       url(r'^facebook_login_success/?$',
                           'common.views.facebook_login_success'),
                       url(r'^search/?$', 'common.views.search'),
                       url(r'^register/?$', 'common.views.register'),
                       url(r'^profile/?$', 'common.views.userprofile'),
                       url(r'^user/(?P<user_name>.*)', 'common.views.user'),
                       url(r'^about/?$', 'common.views.about'),
                       url(r'^privacypolicy/?$', 'common.views.privacypolicy'),
                       url(r'^lang/(?P<lang>\w+)', 'common.views.setlang'),
                       url(r'^contact/success/?$',
                           'common.views.contact_success'),

                       # MODULE BRACELET
                       url(r'^bracelet/photos/(?P<bracelet_id>\d+)/?$',
                           'bracelet.views.photos'),
                       url(r'^bracelet/photoUpload/(?P<bracelet_id>\d+)',
                           'bracelet.views.photo_upload'),
                       url(r'^bracelet/photo/remove/(?P<photo_id>\d+)',
                           'bracelet.views.delete_photo'),
                       url(r'^bracelet/remove/(?P<bracelet_id>\d+)/?$',
                           'bracelet.views.delete_bracelet'),
                       url(r'^bracelet/rate/(?P<bracelet_id>\d+)/(?P<bracelet_rate>\d+)/?$',
                           'bracelet.views.rate'),
                       url(r'^bracelet/rate/remove/(?P<rate_id>\d+)',
                           'bracelet.views.delete_rate'),
                       url(r'^bracelet/change_status/(?P<bracelet_id>\d+)$',
                           'bracelet.views.change_status'),
                       url(r'^bracelet/generate/(?P<pattern_text>.+)/(?P<text_height>.+)/?$',
                           'bracelet.views.generate_text_pattern'),
                       url(r'^bracelet/delete/(?P<bracelet_id>\d+)/?$',
                           'bracelet.views.delete_bracelet'),
                       url(r'^bracelet/edit/(?P<bracelet_id>\d+)/?$',
                           'bracelet.views.edit_bracelet'),
                       url(r'^bracelet/accept/(?P<bracelet_id>\d+)/(?P<bracelet_status>\-?\d?)/?$',
                           'bracelet.views.accept'),
                       url(r'^add/(?P<bracelet_type>.*)/?$',
                           'bracelet.views.add'),
                       url(r'^addpattern/?$', 'bracelet.views.addpattern'),
                       url(r'^bracelet/(?P<bracelet_url>.+)?$',
                           'bracelet.views.bracelet'),

                       # MODULE COMMENT
                       url(r'^comments/(?P<bracelet_id>\d+)/$',
                           'comments.views.pattern_comments'),
                       url(r'^comments/post/$',
                           'comments.views.pattern_comments_post'),
                       url(r'^comments/posted/$',
                           'comments.views.pattern_comments_posted'),
                       url(r'^comments/', include('django.contrib.comments.urls')),

                       # MODULE ADMIN
                       url(r'admin/manage_bracelets/?',
                           'admin.views.manage_bracelets'),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/',
                       # include('django.contrib.admindocs.urls')),

                       url(r'^password_change/?$',
                           'django.contrib.auth.views.password_change', name='password_change'),
                       url(r'^password_change/done/?$',
                           'django.contrib.auth.views.password_change_done', name='password_change_done'),
                       url(r'^password_reset/?$',
                           'django.contrib.auth.views.password_reset', name='password_reset'),
                       url(r'^password_reset/done/?$',
                           'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$',
                           'django.contrib.auth.views.password_reset_confirm',
                           name='password_reset_confirm'),
                       url(r'^reset/done/?$', 'django.contrib.auth.views.password_reset_complete',
                           name='password_reset_complete'),

                       # Uncomment the next line to enable the admin:
                       url(r'^superadmin/', include(admin.site.urls)),
                       )

urlpatterns += staticfiles_urlpatterns()
