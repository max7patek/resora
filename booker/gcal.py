import os
from datetime import timedelta
import datetime
import pytz
from collections import namedtuple

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


#global
service_account_email = 'office-hour-booker@algorithmsbooker.iam.gserviceaccount.com'
CLIENT_SECRET_FILE = 'secrets/AlgorithmsBooker-f554b310351f.json'
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


def events_within(starttime, endtime=None):
    if endtime is None:
        endtime = starttime + datetime.timedelta(hours=24)
    service = get_service()
    page_token = None
    while True:
        resp = service.events().list(
            calendarId=default_cal['id'],
            pageToken=page_token,
            timeMin=starttime.isoformat(),
            timeMax=endtime.isoformat(),
        ).execute()
        yield from resp['items']
        page_token = resp.get('nextPageToken')
        if not page_token:
            break

def grant_write_permission(email):
    service = get_service()
    rule = {
        'scope': {
            'type': 'user',
            'value': email,
        },
        'role': 'writer',
    }
    return service.acl().insert(calendarId=default_cal['id'], body=rule).execute()['id']


def remove_write_permission(email):
    service = get_service()
    for rule in all_rule():
        if rule['scope']['type'] == 'user' and rule['scope']['value'] == email:
            service.acl().delete(calendarId=default_cal['id'], ruleId=rule['id'])


def all_rules():
    service = get_service()
    page_token = None
    while True:
        resp = service.acl().list(
            calendarId=default_cal['id'],
            pageToken=page_token,
        ).execute()
        yield from resp['items']
        page_token = resp.get('nextPageToken')
        if not page_token:
            break

def parse_datetime(cal_datetime):
    return datetime.datetime.fromisoformat(cal_datetime)
