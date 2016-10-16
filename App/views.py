from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from App import forms

from .models import *

@login_required(login_url="login/")

def home(request):
	if request.user.is_superuser:
		user = User.objects.get(username=request.user.username)
		return render(request,"home.html", {'user':user})
	if request.user.is_authenticated():
		user_temp = User.objects.get(username=request.user.username)
		user = ModelUser.objects.get(user=user_temp)
		context = {
			'user': user
		}
		return render(request,"App/home.html", context=context)
	return HttpResponseRedirect('/login')


def register(request):
	if not request.user.is_authenticated():
		if request.method == "POST":
			form1 = forms.UserSignUpForm(request.POST)
			form2 = forms.ModelUserSignup(request.POST)
			if form1.is_valid() and form2.is_valid():
				user = form1.save(commit=False)
				user.password = make_password(form1.cleaned_data['password'])
				user.email = form1.cleaned_data['email']
				user.save()
				user1 = form2.save(commit=False)
				user1.user = user
				user1.save()
				return HttpResponseRedirect('/')
		else:
			form1 = forms.UserSignUpForm()
			form2 = forms.ModelUserSignup()
		return render(request,'App/register.html',context={
			'form':form1,
			'form1':form2
			})
	else:
		messages.error(request, 'You Are logged In')
		return redirect('/')


def change_password(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user)
				messages.success(request, 'Your password was successfully updated!')
				return redirect('/')
			else:
				messages.error(request, 'Please correct the error below.')
		else:
			form = PasswordChangeForm(request.user)
		return render(request, 'App/change_password.html', {
			'form': form
		})
	else:
		messages.error(request, 'You Are not logged In')
		return redirect('/')

@login_required(login_url='login/')
def discuss(request):
	expert_discuss = ModelDiscuss.objects.filter(source='expert').order_by('-timestamp')[:10]
	doctor_discuss = ModelDiscuss.objects.filter(source='doctor').order_by('-timestamp')[:10]
	user_discuss = ModelDiscuss.objects.filter(source='user').order_by('-timestamp')[:10]

	context = {
		'expert': expert_discuss,
		'doctor': doctor_discuss,
		'user': user_discuss
	}
	return render(request, 'App/viewdiscuss.html', context)

@login_required(login_url='login/')
def createDiscuss(request):
	if request.user.is_superuser:
		user = User.objects.get(username=request.user.username)
	else:
		user_temp = User.objects.get(username=request.user.username)
		user = ModelUser.objects.get(user=user_temp)
	if request.method == 'POST':
		DiscussForm = forms.DiscussForm(request.POST)
		if DiscussForm.is_valid():
			form = DiscussForm.save(commit=False)
			if hasattr(user,'role'):
				form.source = user.role
			else:
				form.source = 'expert'
			form.user = user
			form.save()
			return HttpResponseRedirect('/discuss/')
	if request.method == 'GET':
		DiscussForm = forms.DiscussForm()
	return render(request, 'App/createDiscuss.html', context={'form':DiscussForm})

@login_required(login_url='login/')
def question(request):
	questions = ModelQuestion.objects.all().order_by('-timestamp')[:20]
	return render(request, 'App/viewQuestions.html', context={'questions': questions})

@login_required(login_url='login/')
def answer(request, pk):
	try:
		question = ModelQuestion.objects.get(pk=pk)
	except ModelQuestion.DoesNotExist:
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = User.objects.get(username=request.user.username)
			form.ques = ModelQuestion.objects.get(pk=pk)
			form.save()
			return HttpResponseRedirect('/questions')
	if request.method == 'GET':
		form = AnswerForm()
		return render(request, 'App/answer.html', context={'form': form})
	return HttpResponseRedirect('/')

@login_required(login_url='login/')
def postQuestion(request):
	if request.method == 'POST':
		form = forms.QuestionForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = User.objects.get(username=request.user.username)
			form.save()
			return render(request, 'App/postQuestion.html', context={'form': form})
	if request.method == 'GET':
		form = forms.QuestionForm()
		return render(request, 'App/postQuestion.html', context={'form': form})
	return HttpResponseRedirect('/')

@login_required(login_url='login/')
def viewQuestion(request,pk):
	try:
		question = ModelQuestion.objects.get(pk=pk)
	except ModelQuestion.DoesNotExist:
		return HttpResponseRedirect('/questions/')
	try:
		answers = ModelAnswer.objects.filter(ques=question).order_by('-timestamp')[:7]
	except ModelAnswer.DoesNotExist:
		answers = []
	context = {
		'question': question,
		'answers': answers
	}
	print context
	return render(request, 'App/viewQuestion.html', context=context)