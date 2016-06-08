from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction

from .models import Topic, Question, Answer, Comment, Post, UserProfile, UserFollows, Notification, UserTopics
from .forms import QuestionForm, AnswerForm, CommentForm, DeletePostForm, UserProfileForm, FollowForm, UpvotesForm, SeekForm, SeekConfirmForm
from .utils import notification_create

def login(request):
    return render_to_response('quorapp/login.html')

@login_required(login_url = '/')
def home(request):
    questions = Question.objects.filter(isactive = 1).order_by('-updated_at')
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)

    return render(request,'quorapp/home.html',{'request': request,'user': request.user,
        'topicslist':topics,'questionslist':questions,'notifications':notifications})

@login_required(login_url = '/')
def topic_questions(request):
    user_topics = UserTopics.objects.filter(user_id = request.user.id)
    topics_following = []
    for topic in user_topics:
        topics_following.append(topic.topic_id)
    questions = Question.objects.filter(topic_id__in = topics_following,isactive =1).order_by('-updated_at')
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)

    return render(request,'quorapp/home.html',{'request': request,'user': request.user,
        'topicslist':topics,'questionslist':questions,'notifications':notifications})

@login_required(login_url = '/')
def follow_questions(request):
    user_follows = UserFollows.objects.filter(user_id = request.user.id)
    user_following = []
    for user in user_follows:
        user_following.append(user.follow_id)
    questions = Question.objects.filter(user_id__in = user_following,isactive =1).order_by('-updated_at')
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)

    return render(request,'quorapp/home.html',{'request': request,'user': request.user,
        'topicslist':topics,'questionslist':questions,'notifications':notifications})

@login_required(login_url = '/')
def view_profile(request):
    user_id = request.GET.get("u",request.user.id)
    topics = Topic.objects.all()
    notifications = Notification.objects.filter(notification_id = request.user.id)
    if int(user_id) == int(request.user.id):
        following = UserFollows.objects.filter(user_id = request.user.id)
        followers = UserFollows.objects.filter(follow_id = request.user.id)
        topics_following = UserTopics.objects.filter( user_id = request.user.id)
        remove = 1
    else:
        following = UserFollows.objects.filter(user_id = user_id)
        followers = UserFollows.objects.filter(follow_id = user_id)
        topics_following = UserTopics.objects.filter( user_id = user_id)
        remove = 0
    try:
        profile = UserProfile.objects.get(user_id = user_id)
        return render(request,'quorapp/view_profile.html',
                {'topicslist':topics,'profile':profile,
                    'following':following,
                    'followers':followers,
                    'topics_following':topics_following,
                    'notifications':notifications,
                    'remove':remove})
    except:
        return render(request,'quorapp/error.html',{'topicslist':topics,'notifications':notifications})

@login_required(login_url = '/')
def edit_profile(request):
    profile = UserProfile.objects.get(user_id = request.user.id)
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form = UserProfileForm(initial = {
            'first_name':profile.first_name,
            'last_name':profile.last_name,
            'about':profile.about,
            'age':profile.age,
            'sex':profile.sex,
            'website':profile.website,
            'profileimage':profile.profileimage,
            })
    else:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = UserProfile.objects.get(user_id = request.user.id)
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.about = form.cleaned_data['about']
            profile.age = form.cleaned_data['age']
            profile.sex = form.cleaned_data['sex']
            profile.website = form.cleaned_data['website']
            profile.profileimage = form.cleaned_data['profileimage']
            profile.save()

            return HttpResponseRedirect('/view_profile/?status=Profile Saved')

    return render(request,'quorapp/profile.html',{'form':form,'topicslist':topics,'notifications':notifications})

@login_required(login_url = '/')
def postquestion(request):
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(request.POST)
        if form.is_valid():
            topic = Topic.objects.filter(id=int(form.cleaned_data['topics'])).first()
            question = Question.objects.create(
                type = 'quorapp.question',
                user = request.user,
                text = form.cleaned_data['text'],
                topic = topic
                )
            return HttpResponseRedirect(reverse('quorapp:home'))

    return render(request,'quorapp/postquestion.html',
            {'form':form,'topicslist':topics,'notifications':notifications})

@login_required(login_url = '/')
def postanswer(request):
    question_id = request.GET.get("q")
    question = Question.objects.get(id= question_id)
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                answer = Answer.objects.create(
                    type = 'quorapp.answer',
                    user = request.user,
                    text = form.cleaned_data['text'],
                    imagepath = form.cleaned_data['imagepath'],
                    question_id = question.id,
                    )
                notification_create(question.id,2,question.user.id,request.user.id)
            return HttpResponseRedirect(reverse('quorapp:home'))

    return render(request,'quorapp/postanswer.html',
            {'form':form,'topicslist':topics,'question':question.text,'notifications':notifications})

@login_required(login_url = '/')
def postcomment(request):
    answer_id = request.GET.get("a")
    answer = Answer.objects.get(id= answer_id)
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                comment = Comment.objects.create(
                    type = 'quorapp.comment',
                    user = request.user,
                    text = form.cleaned_data['text'],
                    answer_id = answer.id,
                    )
                notification_create(answer.id,3,answer.user.id,request.user.id)
            return HttpResponseRedirect(reverse('quorapp:home'))

    return render(request,'quorapp/postcomment.html',
            {'form':form,'topicslist':topics,'answer':answer.text,'notifications':notifications})

@login_required(login_url = '/')
def postdelete(request):
    post_id = request.GET.get("p")
    if request.method == 'GET':
        topics = Topic.objects.all()
        notifications = Notification.objects.filter (notification_id = request.user.id)
        post = Post.objects.get(id = post_id)
        form = DeletePostForm()
    else:
        post = Post.objects.get(id= post_id)
        if request.user == post.user:
            post.delete()

        return HttpResponseRedirect(reverse('quorapp:home'))

    return render(request,'quorapp/postdelete.html',{'form':form,'topicslist':topics,'post':post.text,'notifications':notifications})

@login_required(login_url = '/')
def topic(request):
    topic_id = request.GET.get("t",1)
    questions = Question.objects.filter(topic_id = topic_id,isactive = 1).order_by('-updated_at')
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)

    return render(request,'quorapp/home.html',{'topicslist':topics,'questionslist':questions,'notifications':notifications})

@login_required(login_url = '/')
def follow_topic(request):
    topic_id = request.GET.get("t",1)
    topic_follow = UserTopics.objects.create(
            topic_id = topic_id,
            user_id = request.user.id,
            )
    return HttpResponseRedirect('/home/?status=Topic Followed')

@login_required(login_url = '/')
def follow(request):
    follow_id = request.GET.get("f")
    follow = User.objects.get(id = follow_id)
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form  = FollowForm()
    else:
        user_follows = UserFollows.objects.create(
                user = request.user,
                follow_id = follow.id,
                )

        return HttpResponseRedirect(reverse('quorapp:home'))

    return render(request,'quorapp/follow.html',{'topicslist':topics,'follow':follow,'notifications':notifications})

@login_required(login_url = '/')
def upvote(request):
    upvote_id = request.GET.get("u")
    answer = Answer.objects.get(id = upvote_id)
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form = UpvotesForm()
    else:
        answer.upvotes += 1
        answer.save()

        return HttpResponseRedirect(reverse('quorapp:home'))

    return render(request,'quorapp/upvote.html',{'topicslist': topics,'answer':answer.text,'notifications':notifications})

@login_required(login_url = '/')
def seek(request):
    question_id = request.GET.get("q",1)
    question = Question.objects.get(id = question_id,isactive = 1).order_by('-updated_at')
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form = SeekForm()
    else:
        form = SeekForm(request.POST)
        if form.is_valid():
            users = User.objects.filter(username__icontains = form.cleaned_data['search'])

            return render(request,'quorapp/seek.html',{'form':form,'topicslist':topics,'question':question,'users':users,'notifications':notifications})

    return render(request,'quorapp/seek.html',{'form':form,'topicslist':topics,'question':question,'notifications':notifications})

@login_required(login_url = '/')
def seek_confirm(request):
    question_id = request.GET.get("q",1)
    user_id = request.GET.get("u",1)
    question = Question.objects.get(id = question_id,isactive = 1).order_by('-updated_at')
    user = User.objects.get(id = user_id)
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)
    if request.method == 'GET':
        form = SeekConfirmForm()
    else:
        notification_create(question_id,1,user_id,request.user.id)

        return HttpResponseRedirect('/home/?status=Question Asked')

    return render(request,'quorapp/seek_confirm.html',{'form':form,'topicslist':topics,'question':question,'user':user,'notifications':notifications})

@login_required(login_url = '/')
def question(request):
    question_id = request.GET.get("q",1)
    question = Question.objects.filter(id = question_id,isactive = 1).order_by('-updated_at')
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)

    return render(request,'quorapp/home.html',{'topicslist':topics,'questionslist':question,'notifications':notifications})

@login_required(login_url = '/')
def notification(request):
    notification_id = request.GET.get("n",1)
    notification = Notification.objects.get(id = notification_id)
    notification.read = 1
    notification.save()
    question = Question.objects.filter(id = notification.post_id,isactive = 1).order_by('-updated_at')
    topics = Topic.objects.all()
    notifications = Notification.objects.filter (notification_id = request.user.id)

    return render(request,'quorapp/home.html',{'topicslist':topics,'questionslist':question,'notifications':notifications})

@login_required(login_url = '/')
def remove(request):
    remove = request.GET.get("r",1)



