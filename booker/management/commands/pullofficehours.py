from django.core.management.base import BaseCommand

from booker.gcal import events_within

from booker.models import OfficeHour

import datetime
import pytz


class Command(BaseCommand):
    help = "'pullofficehours' grabs events on the google calendar within the \n \
            next numhours and creates office hours and bookables for them."

    def add_arguments(self, parser):
        parser.add_argument('hours', type=int)

    def handle(self, *args, **options):
        now = datetime.datetime.now(pytz.timezone('America/New_York'))
        for event in events_within(now, now + datetime.timedelta(hours=options['hours'])):
            if len(OfficeHour.objects.filter(event_id=event['id'])) > 0:
                self.stdout.write('Event at %s has already been pulled.' % event['start']['dateTime'])
            else:
                oh = OfficeHour.make_from_event(event)
                self.stdout.write(self.style.SUCCESS(
                    'Successfully pulled office hour for %s' % oh.starttime
                ))
