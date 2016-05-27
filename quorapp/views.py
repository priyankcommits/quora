from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from .models import Topic, Question, Answer, Post, UserProfile
from .forms import QuestionForm, AnswerForm, DeletePostForm, UserProfileForm

def login(request):
    return render_to_response('quorapp/login.html')

@login_required(login_url = '/')
def home(request):
    questions = Question.objects.all().order_by('-updated_at')
    # answers = Answer.objects.all()
    topics = Topic.objects.all()
    print topics
    context = RequestContext(request,{'request': request,'user': request.user,
        'topicslist':topics,'questionslist':questions})

    return render_to_response('quorapp/home.html',context_instance=context)

def profile(request):
    profile = UserProfile.objects.get(user_id =1)
    topics = Topic.objects.all()
    if request.method == 'GET':
        form = UserProfileForm(instance = profile)
    else:
        pass

    return render(request,'quorapp/profile.html',{'form':form,'topicslist':topics})

def postquestion(request):
    topics = Topic.objects.all()
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(request.POST)
        if form.is_valid():
            topic = Topic.objects.filter(id = int(form.cleaned_data['topics'])).first()
            question = Question.objects.create(
                type = 'quorapp.question',
                user = request.user,
                text = form.cleaned_data['text'],
                topic = topic
                )
            return HttpResponseRedirect('/home/')

    return render(request,'quorapp/postquestion.html',{'form':form,'topicslist':topics})

def postanswer(request):
    question_id = request.GET.get("q")
    question = Question.objects.get(id= question_id)
    if request.method == 'GET':
        topics = Topic.objects.all()
        form = AnswerForm()
    else:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(
                type = 'quorapp.answer',
                user = request.user,
                text = form.cleaned_data['text'],
                imagepath = form.cleaned_data['imagepath'],
                question_id = question.id,
                )
            return HttpResponseRedirect('/home/')

    return render(request,'quorapp/postanswer.html',{'form':form,'topicslist':topics,'question':question.text})

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

