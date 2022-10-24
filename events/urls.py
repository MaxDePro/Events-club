from django.urls import path
from.views import *

urlpatterns = [
    path('', home, name='home'),
    path('<int:year>/<str:month>/', home, name='home'),
    path('events/', events_list, name='events_list'),
    path('event/create/', create_event, name='create_event'),
    path('event_update/<event_id>/', event_update, name='event_update'),
    path('event_delete/<event_id>/', event_delete, name='event_delete'),

    path('venue_list/', list_of_venue, name='venue_list'),
    path('venue_detail/<venue_id>/', venue_detail, name='venue_detail'),
    path('search_venue/', search_venue, name='search_venue'),
    path('venue/create/', create_venue, name='create_venue'),
    path('venue_update/<venue_id>/', venue_update, name='venue_update'),
    path('venue_delete/<venue_id>/', venue_delete, name='venue_delete'),
    path('venue_text', venue_text, name='venue_text'),
    path('venue_csv', venue_csv, name='venue_csv'),
]
