from django.core.management.base import BaseCommand

from booker.models import OfficeHour, Calendar
import mysite.settings as settings

import datetime
import pytz


class Command(BaseCommand):
    help = "'pullofficehours' grabs events on the google calendar within the \n \
            next numhours and creates office hours and bookables for them."

    def add_arguments(self, parser):
        parser.add_argument('hours', type=int)

    def handle(self, *args, **options):
        now = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
        for cal in Calendar.objects.filter(minutes_per_booking__gt=0):
            for event in cal.events_within(now, now + datetime.timedelta(hours=options['hours'])):
                if OfficeHour.objects.filter(event_id=event['id']).exists():
                    self.stdout.write('Event at %s has already been pulled.' % event['start']['dateTime'])
                    if 'location' in event:
                        self.stdout.write('Updating location for event at %s.' % event['start']['dateTime'])
                        for oh in OfficeHour.objects.filter(event_id=event['id']):
                            oh.location = event['location']
                            oh.save()
                else:
                    oh = OfficeHour.make_from_event(event, cal.minutes_per_booking)
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully pulled office hour for %s' % oh.starttime
                    ))
