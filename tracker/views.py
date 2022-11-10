from urllib.robotparser import RequestRate
from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'tracker/home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'tracker/login.html', {'message': 'Invalid Credentials'})

    return render(request, 'tracker/login.html')

def register(request):

    if request.method == "POST":
        name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["cpassword"]
        user_type = request.POST["user_type"]

        if password == password2:
            user = User.objects.create_user(name, email=email,password=password,user_type=user_type)
            user.save()
            user = authenticate(request, username=name, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, 'tracker/register.html', {'message': 'Passwords do not match'})


    return render(request, 'tracker/register.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))