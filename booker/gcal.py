import os
from datetime import timedelta
import datetime
import pytz
from collections import namedtuple

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()


#global
service_account_email = 'office-hour-booker@algorithmsbooker.iam.gserviceaccount.com'
CLIENT_SECRET_FILE = '/secrets/service_creds.json'
SCOPES = 'https://www.googleapis.com/auth/calendar'
scopes = [SCOPES]
default_cal = {
    'kind': 'calendar#calendar',
    'etag': '"2IG_UfzQLHbZ3_DsNnNPPvIpYxU/03vWfKLFalaz0L9Gm7obQolUlho"',
    'id': 'nibko385n9mv06rudr4u0qk9ng@group.calendar.google.com',
    'summary': 'Algorithms',
    'timeZone': 'America/New_York',
    'conferenceProperties': {
        'allowedConferenceSolutionTypes': ['eventHangout']
    }
}

def _build_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filename=CLIENT_SECRET_FILE,
        scopes=SCOPES
    )
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)
    return service

_service = _build_service()

def get_service():
    # check if service still valid
    return _service

def parse_datetime(cal_datetime):
    return datetime.datetime.fromisoformat(cal_datetime)
