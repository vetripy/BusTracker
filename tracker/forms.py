from dataclasses import field
from .models import Bookings, Bus, Route
from django import forms
from django.forms import ModelForm, Form

class BookingsForm(ModelForm):
    bus = forms.ModelChoiceField(queryset=Bus.objects.all(), label='Bus', widget=forms.Select(attrs={'class': 'form-control input-field'}))
    date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-date input-field'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control input-field', 'id': 'time'}))
    route = forms.ModelChoiceField(queryset=Route.objects.all(), label='Route', widget=forms.Select(attrs={'class': 'form-control input-field'}))

    class Meta:
        model = Bookings
        fields = ['bus', 'date', 'time', 'route']

class RouteForm(Form):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), empty_label="--Select Route--", widget=forms.Select(attrs={'class': 'route-field', 'id': 'routeNo'}))