from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from typedmodels.models import TypedModel


class Post(TypedModel):
    text = models.CharField(max_length = 10000)
    user = models.ForeignKey(User)
    isactive = models.BooleanField(default = True)
    isspam = models.BooleanField(default = False)
    imagepath = models.CharField(max_length = 200)


class Topic(models.Model):
    name = models.CharField(max_length = 50)


class Question(Post):
    topic = models.ForeignKey(Topic)


class Answer(Post):
    upvotes = models.IntegerField(default = 0)
    question = models.ForeignKey(Question)


class UserTopics(models.Model):
    user = models.OneToOneField(User)
    topic = models.ForeignKey(Topic)


class UserFollows(models.Model):
    user = models.ForeignKey(User, related_name = 'userfollow')
    follow = models.ForeignKey(User, related_name = 'follow')


class UserFollowers(models.Model):
    user = models.ForeignKey(User ,related_name = 'userfollowers')
    follower = models.ForeignKey(User , related_name = 'follower')
