from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from config import MINUTES_PER_BOOKING
import datetime

from booker.gcal import get_service, parse_datetime


class Calendar(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=25)
    bookable = models.BooleanField()

    def events_within(self, starttime, endtime=None):
        if endtime is None:
            endtime = starttime + datetime.timedelta(hours=24)
        service = get_service()
        page_token = None
        while True:
            resp = service.events().list(
                calendarId=self.id,
                pageToken=page_token,
                timeMin=starttime.isoformat(),
                timeMax=endtime.isoformat(),
            ).execute()
            yield from resp['items']
            page_token = resp.get('nextPageToken')
            if not page_token:
                break

    def grant_write_permission(self, email):
        service = get_service()
        rule = {
            'scope': {
                'type': 'user',
                'value': email,
            },
            'role': 'writer',
        }
        return service.acl().insert(calendarId=self.id, body=rule).execute()['id']


    def remove_write_permission(self, email):
        service = get_service()
        for rule in self.all_rules():
            if rule['scope']['type'] == 'user' and rule['scope']['value'] == email:
                service.acl().delete(calendarId=self.id, ruleId=rule['id'])


    def all_rules(self):
        service = get_service()
        page_token = None
        while True:
            resp = service.acl().list(
                calendarId=self.id,
                pageToken=page_token,
            ).execute()
            yield from resp['items']
            page_token = resp.get('nextPageToken')
            if not page_token:
                break

@receiver(post_save, sender=Calendar)
def add_permission_upon_add_calendar(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        for ta in TA.objects.all():
            instance.grant_write_permission(ta.email)

@receiver(pre_delete, sender=Calendar)
def remove_gcalendar(sender, **kwargs):
    instance = kwargs['instance']
    service = get_service()
    calendar_id = self.id
    service.calendars().delete(calendarId=calendar_id).execute()


class TA(models.Model):
    email = models.CharField(max_length=50)

class Student(models.Model):
    email = models.CharField(max_length=50)

@receiver(post_save, sender=TA)
def add_permission_upon_add_ta(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        for cal in Calendar.objects.all():
            cal.grant_write_permission(instance.email)

@receiver(pre_delete, sender=TA)
def remove_permission(sender, **kwargs):
    instance = kwargs['instance']
    for cal in Calendar.objects.all():
        cal.remove_write_permission(instance.email)



class OfficeHour(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=20, default='contact staff')
    event_id = models.CharField(max_length=50, unique=True, default='no event')

    @classmethod
    def make_from_event(cls, event):
        self = cls()
        self.starttime = parse_datetime(event['start']['dateTime'])
        self.endtime = parse_datetime(event['end']['dateTime'])
        self.location = event['location']
        self.event_id = event['id']
        self.save()
        return self


class Bookable(models.Model):
    officehour = models.ForeignKey('OfficeHour', on_delete=models.CASCADE)
    starttime = models.DateTimeField()

    @classmethod
    def make(cls, officehour, starttime):
        self = cls()
        self.officehour = officehour
        self.starttime = starttime
        self.save()
        return self


@receiver(post_save, sender=OfficeHour)
def spawn_bookables(sender, **kwargs):
    instance = kwargs['instance']
    t = instance.starttime
    while t < instance.endtime:
        Bookable.make(instance, t)
        t = t + datetime.timedelta(minutes=MINUTES_PER_BOOKING)
