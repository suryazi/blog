from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='post_list'),
    url(r'^drafts/$', views.DraftView.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.NewView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.PublishView.as_view(), name='post_publish'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>[0-9]+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>[0-9]+)/remove/$', views.comment_remove, name='comment_remove'),
]
