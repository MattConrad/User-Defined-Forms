from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ckpoc/', include('ckpoc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
        'c:/work/legalcap/ckpoc/static'}),
    (r'^$', 'ckpoc.userforms.views.index'),
    (r'^(?P<user_form_id>\d+)/$', 'ckpoc.userforms.views.index'),
    (r'^new_user_form/$', 'ckpoc.userforms.views.new_user_form'),
    (r'^complete_user_form/$', 'ckpoc.userforms.views.complete_user_form'),
)
