from django.contrib import admin
from .models import Post, Topic, Question, Answer, UserTopics, UserFollows, UserFollowers

# Register your models here.

admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserTopics)
admin.site.register(UserFollows)
admin.site.register(UserFollowers)


