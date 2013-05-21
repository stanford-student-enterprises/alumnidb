from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('alumnidb.database.views',
    url(r'profile/edit/$', 'edit_profile'),
    url(r'profile/all/$', 'all'),
    url(r'profile/current/$', 'current'),
    url(r'profile/(?P<user_id>\d+)/$', 'profile'),
    url(r'profile/(?P<user_id>\d+)/edit/$', 'admin_edit_profile'),
    url(r'profile/(?P<user_id>\d+)/sse_positions/add/$', 'add_sse_position'),
    url(r'profile/(?P<user_id>\d+)/sse_positions/(?P<position_id>\d+)/edit/$', 'edit_sse_position'),
    url(r'profile/(?P<user_id>\d+)/sse_positions/(?P<position_id>\d+)/delete/$', 'delete_sse_position'),
    url(r'profile/$', 'my_profile'),
    url(r'search/$', 'search'),
)