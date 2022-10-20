from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import *
from .forms import *


def create_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/create_venue.html', context={'form': form, 'submitted': submitted})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    name = 'John'

    now = datetime.now()
    cur_year = now.year
    cur_time = now.strftime('%I:%M %p')

    cal = HTMLCalendar().formatmonth(year, month_number)

    context = {
        'name': name,
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'cur_year': cur_year,
        'cur_time': cur_time,
    }
    return render(request, 'events/home.html', context)


def events_list(request):
    list_events = Event.objects.all()

    context = {
        'list_events': list_events
    }
    return render(request, 'events/events_list.html', context)


