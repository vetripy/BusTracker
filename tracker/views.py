from urllib.robotparser import RequestRate
from django.shortcuts import render
from .models import User, Announcements, Bookings,Bus, Route
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import BookingsForm, RouteForm
from django.http import JsonResponse
# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'tracker/home.html')

@login_required(login_url='login')
def tracker(request):
    return render(request, 'tracker/track.html', {'form': RouteForm()})

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

    booked_users = [] 

    for slot in slots:
        for user in slot.users.all():
            booked_users.append(user.username)

    return render(request, 'tracker/bookings.html', {'slots': slots, 'booked_users': booked_users})

@login_required(login_url='login')
def addwbus(request):
    if request.method == "POST":

        form = BookingsForm(request.POST)
        if form.is_valid():
            bus = form.cleaned_data["bus"]
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            route = form.cleaned_data["route"]
            slot = Bookings(bus=bus, date=date, time=time, route=route)
            slot.save()
            
        return HttpResponseRedirect(reverse("bookings"))

    return render(request, 'tracker/addwbus.html',{'form': BookingsForm()})

@login_required(login_url='login')
def deletebus(request, code):
    if request.user.user_type == 'inc':
        slot = Bookings.objects.get(id=code)
        slot.delete()
    return HttpResponseRedirect(reverse("bookings"))

@login_required(login_url='login')
def bookbus(request, code, user):
    if request.user.user_type == 'hos':
        slot = Bookings.objects.get(id=code)
        cus = User.objects.get(id=user)

        if slot.bus_capacity > 0:
            slot.users.add(cus)
            slot.bus_capacity -= 1
            slot.save()
        else:
            return HttpResponseRedirect(reverse("bookings")) 
    return HttpResponseRedirect(reverse("bookings"))

@login_required(login_url='login')
def viewbookings(request, code):
    if request.user.user_type == 'inc':
        bookings = Bookings.objects.get(id=code)

        booked_users = []

        for user in bookings.users.all():
            booked_users.append(user)

        return render(request, 'tracker/viewbookings.html', {'users': booked_users})

    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='login')
def cancelbus(request, code, user):
    if request.user.user_type == 'hos':
        slot = Bookings.objects.get(id=code)
        cus = User.objects.get(id=user)
        if cus in slot.users.all():
            slot.users.remove(cus)
            slot.bus_capacity += 1
            slot.save() 
        
    return HttpResponseRedirect(reverse("bookings"))

@csrf_exempt
@login_required(login_url='login')
def route(request, code):
    """Returns the route data as a JSON object"""
    route = Route.objects.get(route_no=code)
    
    start = {route.start_stop.stop_lat, route.start_stop.stop_lng}
    waypoints = []

    for waypoint in route.waypoints.all():
        if waypoint.stop_lat and waypoint.stop_lng and start != {waypoint.stop_lat, waypoint.stop_lng}:
            waypoints.append({
                'lat': waypoint.stop_lat,
                'lng': waypoint.stop_lng,
            })

    return JsonResponse({
        "lat": route.start_stop.stop_lat,
        "lng": route.start_stop.stop_lng,
        "waypoints": waypoints
    })

@login_required(login_url='login')
def profile(request, code):
    user = User.objects.get(username=code)
    return render(request, 'tracker/profile.html', {'user': user})