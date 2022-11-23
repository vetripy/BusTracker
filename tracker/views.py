from urllib.robotparser import RequestRate
from django.shortcuts import render
from .models import User, Announcements, Bookings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import BookingsForm
# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'tracker/home.html')

@login_required(login_url='login')
def tracker(request):
    return render(request, 'tracker/track.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(user)
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

@login_required(login_url='login')
def announcements(request):

    announcements = Announcements.objects.all()

    data = []

    for i in range(len(announcements)-1,0,-1):
        data.append({
            'title': announcements[i].title,
            'description': announcements[i].description,
            'date': announcements[i].date,
            'for_user': announcements[i].for_user,
            'id' : announcements[i].id,
        })

    return render(request, 'tracker/announcements.html', {'announcements': data})


@login_required(login_url='login')
def addannouncement(request):
    
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["desc"]
            for_user = request.POST["user_type"] 
            announcement = Announcements(title=title, description=description, for_user=for_user)
            announcement.save()
            return HttpResponseRedirect(reverse("announcements"))
    
        return render(request, 'tracker/addannouncement.html')

@login_required(login_url='login')
def deleteannouncement(request, code):
    announcement = Announcements.objects.get(id=code)
    announcement.delete()
    return HttpResponseRedirect(reverse("announcements"))

@login_required(login_url='login')
def bookings(request):

    slots = Bookings.objects.all()
    return render(request, 'tracker/bookings.html', {'slots': slots})

@login_required(login_url='login')
def addwbus(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        date = request.POST["date"]
        time = request.POST["time"]
        slot = Bookings(name=name, email=email, phone=phone, date=date, time=time)
        slot.save()
        return HttpResponseRedirect(reverse("bookings"))

    return render(request, 'tracker/addwbus.html',{'form': BookingsForm(request=request)})