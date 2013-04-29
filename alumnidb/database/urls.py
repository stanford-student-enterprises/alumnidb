from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('alumnidb.database.views',
    url(r'profile/edit/$', 'edit_profile'),
    url(r'profile/(?P<user_id>\d+)/$', 'profile'),
    url(r'profile/$', 'my_profile'),
    url(r'authenticate/$', 'authenticate'),
)