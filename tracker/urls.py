from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_view, name="logout" ),
    path('announcements', views.announcements, name="announcements"),
    path('tracker', views.tracker, name="tracker"),
    path('bookings', views.bookings, name="bookings"),
    path('addwbus', views.addwbus, name="addwbus"),
    path('addannouncement', views.addannouncement, name="addannouncement"),
    path('deleteannouncement/<int:code>', views.deleteannouncement, name="deleteannouncement"),
    path('deletebus/<int:code>', views.deletebus, name="deletebus"),
    path('bookbus/<int:code>/<int:user>', views.bookbus, name="bookbus"),
    path('cancelbus/<int:code>/<int:user>', views.cancelbus, name="cancelbus"),

]