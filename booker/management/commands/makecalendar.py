from django.core.management.base import BaseCommand

from booker.gcal import get_service

from booker.models import Calendar

import datetime
import pytz


class Command(BaseCommand):
    help = "'makecalendar' creates a google calendar for course events. Can be bookable or not"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('bookable', type=bool)

    def handle(self, *args, **options):
        cal = Calendar()
        body = {
            'summary': options['name'],
            'timeZone': 'America/New_York'
        }
        service = get_service()
        created_calendar = service.calendars().insert(body=body).execute()

        cal.id = created_calendar['id']
        cal.name = options['name']
        cal.bookable = options['bookable']
        cal.save()

        rule = {
            'scope': {
                'type': 'default',
            },
            'role': 'reader'
        }

        created_rule = service.acl().insert(calendarId=cal.id, body=rule).execute()
        self.stdout.write(self.style.SUCCESS(
            'Successfully created calendar %s' % cal.name
        ))
