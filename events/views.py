from django.contrib import messages
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse
# import django user model
from django.contrib.auth.models import User

from .models import *
from .forms import *
import csv

# import pdf tools
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# import pagination toools
from django.core.paginator import Paginator


def venue_events(request, venue_id):
    # Grab the venue
    venue = Venue.objects.get(id=venue_id)
    # Grab the events of that venue
    events = venue.event_set.all()

    if events:
        return render(request, 'events/venue_events.html', {'events': events})
    else:
        messages.success(request, 'Here is no events with this venue')
        return redirect('admin_approved')


def admin_approved(request):
    events_list = Event.objects.all().order_by('-event_date')

    # Get the venue list
    venue_list = Venue.objects.all()

    # Get counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    # Check if user is admin
    if request.user.is_superuser:
        if request.method == 'POST':
            # Get changed in boxes on approved
            events_id = request.POST.getlist('boxes')

            # Uncheck all events because we can't just uncheck box change
            events_list.update(approved=False)

            # Update database
            for box in events_id:
                Event.objects.filter(pk=int(box)).update(approved=True)
            messages.success(request, 'Event has updated')
            return redirect('events_list')
        else:
            return render(request, 'events/admin_approved.html', context={
                'events_list': events_list,
                'event_count': event_count,
                'venue_count': venue_count,
                'user_count': user_count,
                'venue_list': venue_list,
            })
    else:
        messages.success(request, 'You have no root for this action')
        return redirect('home')


def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    users = Event.objects.all().prefetch_related('many_set')
    context = {
        'event': event,
        'users': users,
    }
    return render(request, 'events/event_detail.html', context)


def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)
        return render(request, 'events/search_events.html', {'searched': searched, 'events': events})
    else:
        return render(request, 'events/search_events.html', {})


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(users=me)  # also me = request.user.id
        context = {
            'events': events
        }
        return render(request, 'events/my_events.html', context)
    else:
        messages.success(request, 'You need to login to vies this page')
        return redirect('home')


# Generate a pdf file for venue list
def venue_pdf(request):
    # Create bytestream buffer
    buf = io.BytesIO()

    # create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    text_ob = c.beginText()
    text_ob.setTextOrigin(inch, inch)
    text_ob.setFont('Helvetica', 14)

    lines = []
    venues = Venue.objects.all()

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email)
        lines.append(' ')

    # Loop
    for line in lines:
        text_ob.textLine(line)

    # finish up
    c.drawText(text_ob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Venue.pdf')


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
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event deleted')
        return redirect('events_list')
    else:
        messages.success(request, 'Yo have login as event manager to delete it, Try again')
        return redirect('events_list')


def event_update(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser: # also can be request.user.id == 1
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events_list')
    return render(request, 'events/event_update.html', context={'event': event, 'form': form})


def create_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser: # also can be request.user.id == 1
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user  # logged in user
                event.save()
                # form.save()
                return HttpResponseRedirect('?submitted=True')
    else:
        # just going to the page, not submitting
        if request.user.is_superuser: # also can be request.user.id == 1
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/create_event.html', context={'form': form, 'submitted': submitted})


def venue_update(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
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
    venue_owner = User.objects.get(pk=venue.owner)

    # Grab the events of that venue
    events = venue.event_set.all()

    context = {
        'venue': venue,
        'venue_owner': venue_owner,
        'events': events,
    }
    return render(request, 'events/venue_detail.html', context)


def list_of_venue(request):
    context = {}
    # venue_list = Venue.objects.all().order_by('?')
    venue_list = Venue.objects.all()

    # Set up pagination
    p = Paginator(venue_list, 2)
    page = request.GET.get('page')
    venues = p.get_page(page)

    context = {
        'venue_list': venue_list,
        'venues': venues,
    }
    return render(request, 'events/venue.html', context)


def create_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id # logged in user
            venue.save()
            # form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/create_venue.html', context={'form': form, 'submitted': submitted})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    # convert a month name into  number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # get current year
    now = datetime.now()
    cur_year = now.year
    # get current time
    cur_time = now.strftime('%I:%M %p')

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get query the Events model for data
    event_list = Event.objects.filter(
        event_date__year=year,  # also year = datetime.now().year
        event_date__month=month_number, # month_number = int(month_number)

    )

    context = {
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'cur_year': cur_year,
        'cur_time': cur_time,
        'event_list': event_list,
    }
    return render(request, 'events/home.html', context)


def events_list(request):
    list_events = Event.objects.all().order_by('-event_date')

    context = {
        'list_events': list_events
    }
    return render(request, 'events/events_list.html', context)
