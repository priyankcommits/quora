"""quoraslim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from quorapp.views import *
from quoraslim import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login, name='login'),
    url(r'^home/$', home, name='home'),
    url(r'^view_profile/$', view_profile, name='view_profile'),
    url(r'^edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^postquestion/$', postquestion, name='postquestion'),
    url(r'^postanswer/$', postanswer, name='postanswer'),
    url(r'^postdelete/$', postdelete, name='postdelete'),
    url(r'^topic/$', topic, name='topic'),
    url(r'^follow/$', follow, name='follow'),
    url(r'^upvote/$', upvote, name='upvote'),
    url(r'^seek/$', seek, name='seek'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]
