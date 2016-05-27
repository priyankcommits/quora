from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from typedmodels.models import TypedModel

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profileimage = models.CharField(max_length = 200, null= True, blank = True)
    about = models.CharField(max_length = 200, null = True, blank = True)
    age = models.CharField(max_length = 3, null = True, blank = True)
    sex = models.CharField(max_length=1, null= True, blank = True)
    website = models.CharField(max_length= 200, null = True, blank = True)


class CommonInfo(models.Model):
    created_at = models.DateTimeField(default=timezone.now(), null= True, blank = True)
    updated_at = models.DateTimeField(default=timezone.now(), null = True, blank = True)

    class Meta:
        abstract = True


class Post(TypedModel, CommonInfo):
    text = models.CharField(max_length = 10000)
    user = models.ForeignKey(User)
    isactive = models.BooleanField(default = True)
    isspam = models.BooleanField(default = False)
    imagepath = models.CharField(max_length = 200, null = True, blank = True)


class Topic(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name


class Question(Post):
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return str(self.id)


class Answer(Post):
    upvotes = models.IntegerField(default = 0)
    question = models.ForeignKey(Question)

    def __str__(self):
        return str(self.id)


class UserTopics(models.Model):
    user = models.OneToOneField(User)
    topic = models.ForeignKey(Topic)


class UserFollows(models.Model):
    user = models.ForeignKey(User, related_name = 'userfollow')
    follow = models.ForeignKey(User, related_name = 'follow')


class UserFollowers(models.Model):
    user = models.ForeignKey(User ,related_name = 'userfollowers')
    follower = models.ForeignKey(User , related_name = 'follower')
