from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='forum_index'),

    url(r'^register/$', views.register, name='forum_register'),
    url(r'^login/$', views.login, name='forum_login'),

    url(r'^profile/$', views.profile, name='forum_profile'),

    url(r'^category/(?P<category_id>\d+)/$', views.view_category, name='view_category'),
    #url(r'category/(?P<category_id>\d+)/forum/(?P<forum_id>\d+)/$', views.view_forum, name='view_forum'),
    url(r'^(?P<forum_id>\d+)/$', views.view_forum, name='view_forum'),
    url(r'^(?P<forum_id>\d+)/create-thread/$', views.create_thread, name='create_thread'),
    url(r'^(?P<forum_id>\d+)/thread/(?P<thread_id>\d+)/$', views.view_thread, name='view_thread'),

)
