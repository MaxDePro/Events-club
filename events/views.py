from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from .forms import *
import csv


# Generate a csv file with list of venue
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # create a csv writer
    writer = csv.writer(response)

    venues = Venue.objects.all()

    # add column headings to csv file
    writer.writerow(['Venue name', 'Address', 'Zip_code', 'Phone', 'Web address', 'Email'])

    # write content into list
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.email])

    return response


# Create a txt file with all venues
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # get the content for txt file
    venues = Venue.objects.all()
    lines = []
    # write content into list
    for venue in venues:
        lines.append(
            f'{venue.name}\n {venue.address}\n {venue.phone}\n {venue.zip_code}\n{venue.web}\n{venue.email}\n\n\n')

    # write list into response
    response.writelines(lines)
    return response


def venue_delete(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('venue_list')


def event_delete(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('events_list')


def event_update(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events_list')
    return render(request, 'events/event_update.html', context={'event': event, 'form': form})


def create_event(request):
    submitted = False
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/create_event.html', context={'form': form, 'submitted': submitted})


def venue_update(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venue_list')

    return render(request, 'events/venue_update.html', context={'venue': venue, 'form': form})


def search_venue(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venue.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/search_venue.html', {})


def venue_detail(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    context = {
        'venue': venue
    }
    return render(request, 'events/venue_detail.html', context)


def list_of_venue(request):
    venue_list = Venue.objects.all().order_by('name')
    context = {
        'venue_list': venue_list
    }
    return render(request, 'events/venue.html', context)


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

    now = datetime.now()
    cur_year = now.year
    cur_time = now.strftime('%I:%M %p')

    cal = HTMLCalendar().formatmonth(year, month_number)

    context = {
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'cur_year': cur_year,
        'cur_time': cur_time,
    }
    return render(request, 'events/home.html', context)


def events_list(request):
    list_events = Event.objects.all().order_by('event_date')

    context = {
        'list_events': list_events
    }
    return render(request, 'events/events_list.html', context)
