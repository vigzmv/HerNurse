from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from App import forms
from django.contrib.auth.hashers import make_password


@login_required(login_url="login/")

def home(request):
	return render(request,"home.html")

def register(request):
	if request.method == "POST":
		form1 = forms.UserSignUpForm(request.POST)
		if form1.is_valid():
			user = form1.save(commit=False)
			user.password = make_password(form1.cleaned_data['password'])
			user.email = form1.cleaned_data['email']
			user.save()
			return HttpResponseRedirect('/')
	else:
	 	form1 = forms.UserSignUpForm()
	return render(request,'App/register.html',context={'form':form1})
