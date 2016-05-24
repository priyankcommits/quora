from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from .models import Topic, Question, Answer

def login(request):
    return render_to_response('quorapp/login.html')

@login_required(login_url = '/')
def home(request):
    questions = Question.objects.all()
    topics = Topic.objects.all()
    print topics
    context = RequestContext(request,{'request': request,'user': request.user,
        'topicslist':topics,'questionslist':questions })

    return render_to_response('quorapp/home.html',context_instance=context)
