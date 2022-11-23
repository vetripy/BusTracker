from dataclasses import field
from .models import Bookings, Bus, Route
from django import forms
from django.forms import ModelForm

class BookingsForm(ModelForm):
    bus = forms.ChoiceField(label='Bus', widget=forms.Select(attrs={'class': 'input-field'}))
    date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'input-field'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'input-field'}))
    route = forms.ChoiceField(label='Route', widget=forms.Select(attrs={'class': 'input-field'}))

    class Meta:
        model = Bookings
        fields = ['bus', 'date', 'time', 'route']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(BookingsForm, self).__init__(*args, **kwargs)

        buses = []
        for bus_ in Bus.objects.all():
            buses.append((bus_.bus_no, bus_.bus_route))

        if len(buses) != 0:
            self.fields['bus'].choices = buses
        else:
            self.fields['bus'].choices = [('', '--Select Course--')]    

        routes = []
        for route_ in Route.objects.all():
            routes.append((route_.route_no, 'Hi'))

        if len(routes) != 0:
            self.fields['route'].choices = routes
        else:
            self.fields['route'].choices = [('', '--Select Course--')]    