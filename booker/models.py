from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from config import MINUTES_PER_BOOKING
import datetime

from booker.gcal import grant_write_permission, remove_write_permission

class TA(models.Model):
    email = models.CharField(max_length=50)

@receiver(post_save, sender=TA)
def add_permission(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        grant_write_permission(instance.email)

@receiver(pre_delete, sender=TA)
def remove_permission(sender, **kwargs):
    instance = kwargs['instance']
    remove_write_permission(instance.email)



class OfficeHour(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=20, default='contact staff')
    event_id = models.CharField(max_length=50, unique=True, default='no event')

    @classmethod
    def make_from_event(cls, event):
        self = cls()
        self.starttime = time.strptime(event['start']['datetime'], '%Y-%m-%dT%H:%M:%S.%f')
        self.endtime = time.strptime(event['end']['datetime'], '%Y-%m-%dT%H:%M:%S.%f')
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
