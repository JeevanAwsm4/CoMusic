from django.shortcuts import render
from django.contrib.auth import authenticate,login as login_func
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from users.forms import SignupForm

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request,username=username,password=password)
        
            if user is not None:
                login_func(request,user)
                print('authenticated')

                return HttpResponseRedirect("/")
        
        context = {
            "title" : "Error Occured!",
            "error" : True,
            "message" : "Invalid Username or Password",
        }
        return render(request,"auth/login.html",context=context)
    else:
        context = {
            "title" : "Login page",
        }
        return render(request,"auth/login.html",context=context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)

            if not User.objects.filter(username=instance.username).exists():
                user = User.objects.create_user(username=instance.username,password=instance.password,first_name=instance.first_name)
                login_func(request,user)
                print('authenticated')

                return HttpResponseRedirect("/")
            
        context = {
            "title" : "Error Occured!",
            "error" : True,
            "message" : "User Exists!",
            "signup_form" : form,
        }
        return render(request,"auth/signup.html",context=context)
    else:
        form = SignupForm()
        context = {
            "title" : "Signup page",
            "signup_form" : form,
        }
        return render(request,"auth/signup.html",context=context)
