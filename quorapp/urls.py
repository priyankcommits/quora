from django.conf.urls import url, include, patterns
from django.contrib import admin
from quorapp.views import *
from quoraslim import settings

app_name = 'quorapp'
urlpatterns = [
    url(r'^$', login, name='login'),
    url(r'^home/$', home, name='home'),
    url(r'^questions/$', topic_questions, name='topic_questions'),
    url(r'^questions/$', follow_questions, name='follow_questions'),
    url(r'^view_profile/$', view_profile, name='view_profile'),
    url(r'^edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^postquestion/$', postquestion, name='postquestion'),
    url(r'^postanswer/$', postanswer, name='postanswer'),
    url(r'^postcomment/$', postcomment, name='postcomment'),
    url(r'^postdelete/$', postdelete, name='postdelete'),
    url(r'^topic/$', topic, name='topic'),
    url(r'^follow/$', follow, name='follow'),
    url(r'^follow_topic/$', follow_topic, name='follow_topic'),
    url(r'^upvote/$', upvote, name='upvote'),
    url(r'^seek/$', seek, name='seek'),
    url(r'^seek_confirm/$', seek_confirm, name='seek_confirm'),
    url(r'^question/$', question, name='question'),
    url(r'^notification/$', notification, name='notification'),
    url(r'^remove/$', remove, name="remove"),
]

