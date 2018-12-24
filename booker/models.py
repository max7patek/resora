from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from config import MINUTES_PER_BOOKING
import datetime

class OfficeHour(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    location = models.CharField(max_length=20)

    def from_event():
        pass


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
