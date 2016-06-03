from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Topic, Question, Answer, Comment, Post, UserProfile, UserFollows
from .forms import QuestionForm, AnswerForm, DeletePostForm, UserProfileForm, FollowForm, UpvotesForm, SeekForm, SeekConfirmForm

def login(request):
    return render_to_response('quorapp/login.html')

@login_required(login_url = '/')
def home(request):
    questions = Question.objects.all().order_by('-updated_at')
    topics = Topic.objects.all()
    context = RequestContext(request,{'request': request,'user': request.user,
        'topicslist':topics,'questionslist':questions})


    return render_to_response('quorapp/home.html',context_instance=context)

def save_profile(strategy, details, response, user=None, *args, **kwargs):
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
            # attrs = dict(attrs.items() + fb_data.items())
            attrs = dict(attrs.items())
            UserProfile.objects.create(
                **attrs
            )

def view_profile(request):
    user_id = request.GET.get("u",request.user.id)
    profile = UserProfile.objects.get(user_id = user_id)
    topics = Topic.objects.all()

    return render(request,'quorapp/view_profile.html',{'topicslist':topics,'profile':profile})

def edit_profile(request):
    profile = UserProfile.objects.get(user_id = request.user.id)
    topics = Topic.objects.all()
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

    return render(request,'quorapp/profile.html',{'form':form,'topicslist':topics})

def postquestion(request):
    topics = Topic.objects.all()
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
            return HttpResponseRedirect('/home/')

    # import ipdb; ipdb.set_trace()
    return render(request,'quorapp/postquestion.html',
            {'form':form,'topicslist':topics})

def postanswer(request):
    question_id = request.GET.get("q")
    question = Question.objects.get(id= question_id)
    topics = Topic.objects.all()
    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(request.POST)
        # import ipdb; ipdb.set_trace()
        if form.is_valid():
            answer = Answer.objects.create(
                type = 'quorapp.answer',
                user = request.user,
                text = form.cleaned_data['text'],
                imagepath = form.cleaned_data['imagepath'],
                question_id = question.id,
                )
            return HttpResponseRedirect('/home/')

    return render(request,'quorapp/postanswer.html',
            {'form':form,'topicslist':topics,'question':question.text})

def postdelete(request):
    post_id = request.GET.get("p")
    if request.method == 'GET':
        topics = Topic.objects.all()
        post = Post.objects.get(id = post_id)
        form = DeletePostForm()
    else:
        post = Post.objects.get(id= post_id)
        if request.user == post.user:
            post.delete()

        return HttpResponseRedirect('/home/')

    return render(request,'quorapp/postdelete.html',{'form':form,'topicslist':topics,'post':post.text})

def topic(request):
    topic_id = request.GET.get("t",1)
    questions = Question.objects.filter(topic_id = topic_id)
    topics = Topic.objects.all()

    return render(request,'quorapp/home.html',{'topicslist':topics,'questionslist':questions})

def follow(request):
    follow_id = request.GET.get("f")
    follow = User.objects.get(id = follow_id)
    topics = Topic.objects.all()
    if request.method == 'GET':
        form  = FollowForm()
    else:
        user_follows = UserFollows.objects.create(
                user = request.user,
                follow_id = follow.id,
                )

        return HttpResponseRedirect("/home/")

    return render(request,'quorapp/follow.html',{'topicslist':topics,'follow':follow})

def upvote(request):
    upvote_id = request.GET.get("u")
    answer = Answer.objects.get(id = upvote_id)
    topics = Topic.objects.all()
    if request.method == 'GET':
        form = UpvotesForm()
    else:
        answer.upvotes += 1
        answer.save()

        return HttpResponseRedirect(reverse(home))

    return render(request,'quorapp/upvote.html',{'topicslist': topics,'answer':answer.text})

def seek(request):
    question_id = request.GET.get("q",1)
    question = Question.objects.get(id = question_id)
    topics = Topic.objects.all()
    if request.method == 'GET':
        form = SeekForm()
    else:
        form = SeekForm(request.POST)
        # import ipdb; ipdb.set_trace()
        if form.is_valid():
            users = User.objects.filter(username__icontains = form.cleaned_data['search'])

        return render(request,'quorapp/seek.html',{'form':form,'topicslist':topics,'users':users})

    return render(request,'quorapp/seek.html',{'form':form,'topicslist':topics,'question':question})

def seek_confirm(request):
    question_id = request.GET.get("q",1)
    question = Question.objects.get(id = quesiton_id)
    topics = Topic.objects.all()
    if request.method == 'GET':
        form = SeekConfirmForm()
    else:
        Notification(question_id,)

