from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip code', max_length=10, blank=True)
    phone = models.CharField('Contact phone', max_length=15, blank=True)
    web = models.URLField('Website address', blank=True)
    email = models.EmailField('Email address', blank=True)
    owner = models.IntegerField('Venue owner', blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField('User email')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(MyClubUser, blank=True)
    approved = models.BooleanField('Approved event', default=False)

    def __str__(self):
        return self.name

    @property
    def days_to_event(self):
        today = date.today()
        days_till_event = self.event_date.date() - today
        days_till_stripped = str(days_till_event).split(',')[0]
        return days_till_stripped
