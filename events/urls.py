from django.urls import path
from.views import *

urlpatterns = [
    path('', home, name='home'),
    path('<int:year>/<str:month>/', home, name='home'),

    path('events/', events_list, name='events_list'),
    path('event_detail/<event_id>/', event_detail, name='event_detail'),
    path('event/create/', create_event, name='create_event'),
    path('event_update/<event_id>/', event_update, name='event_update'),
    path('event_delete/<event_id>/', event_delete, name='event_delete'),
    path('my_events', my_events, name='my_events'),
    path('search_events', search_events, name='search_events'),
    path('admin_approved', admin_approved, name='admin_approved'),

    path('venue_list', list_of_venue, name='venue_list'),
    path('venue_detail/<venue_id>/', venue_detail, name='venue_detail'),
    path('search_venue/', search_venue, name='search_venue'),
    path('venue/create/', create_venue, name='create_venue'),
    path('venue_update/<venue_id>/', venue_update, name='venue_update'),
    path('venue_delete/<venue_id>/', venue_delete, name='venue_delete'),
    path('venue_events/<venue_id>/', venue_events, name='venue_events'),
    path('venue_text', venue_text, name='venue_text'),
    path('venue_csv', venue_csv, name='venue_csv'),
    path('venue_pdf', venue_pdf, name='venue_pdf'),

]
