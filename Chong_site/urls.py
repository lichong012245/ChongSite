from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


    # Examples:
    url(r'^$', 'Chong_site.views.home', name='home'),
    url(r'^home/$', 'Chong_site.views.home'),
    url(r'^contact/$', 'Chong_site.views.contact',name='contact'),
    url(r'^bio/$', 'Chong_site.views.bio', name='bio'),
    url(r'^disclaimer/$',TemplateView.as_view(template_name='chongsite/disclaimer.html')),
    url(r'^portforlio/$','Chong_site.views.portforlio'),
    url(r'^blog/', include('blog.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^portfolio/pictures/$', 'Chong_site.views.picture', name='picture'),
    url(r'^portfolio/$', 'Chong_site.views.picture', name='picture'),
    url(r'^portfolio/projects/$', 'Chong_site.views.projects', name='project'),
    url(r'^portfolio/misc/$', 'Chong_site.views.misc', name='misc'),


    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    urlpatterns += staticfiles_urlpatterns()

