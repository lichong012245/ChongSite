from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView
from django.views.generic.dates import ArchiveIndexView
from blog.views import Postlist, PostDetailWithComment,TagListView,PostMonthArchiveView,PostArchiveIndexView,tagmap
from blog.models import post




urlpatterns = patterns('',
    url(r'^$',Postlist.as_view()),
    url(r'^tagmap/$',tagmap.as_view(),name='tag_map'),
    url(r'^archive/$',PostArchiveIndexView.as_view(),name="post_archive"),
    url(r'^slug/(?P<slug>[-_\w]+)$', PostDetailWithComment.as_view(),name='postdetailwithcomment'),
    url(r'^tag/([-_\w]+)$', TagListView.as_view(),name='taglistview'),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/$',PostMonthArchiveView.as_view(month_format='%m'),name="archive_month_numeric"),


)


