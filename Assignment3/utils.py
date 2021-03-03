from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

"""
Reference Google Calendar API for more information on usage and functions.

Rest API: https://developers.google.com/calendar/v3/reference

Python API: https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html

"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


def create_event_from_data(summary="", location="", description="", start="",
                           end="", recurrRule=[],
                           attendees=[], defaultReminder=False, reminderOverrides=[]):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': start,
        'end': end,
        'recurrence': recurrRule,
        'attendees': attendees,
        'reminders': {
            'useDefault': defaultReminder,
            'overrides': reminderOverrides,
        },
    }
    return event

def create_calendar(summary="", location="", description="", timeZone=""):
    cal = {
        'summary': summary,
        'location': location,
        'description': description,
        'timeZone': timeZone,
    }
    return cal

def get_calendar_events(num_events=10):
    global service
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=num_events, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

def get_calendar_list(num_results=10):
    global service
    cals = service.calendarList().list(maxResults=num_results).execute()
    cals = cals.get('items', [])

    return cals

def get_calendar_info(calId):
    global service
    cal_info = service.calendars().get(calendarId=calId).execute()
    return cal_info

def get_event_info(eventId):
    global service
    event_info = service.events().get(calendarId='primary', eventId=eventId).execute()

    return event_info

def add_calendar(cal_data):
    global service
    try:
        service.calendars().insert(body=cal_data).execute()
        return True, None
    except HttpError as e:
        return False, e

def add_event(event_data):
    global service
    try:
        service.events().insert(calendarId='primary', body=event_data).execute()
        return True, None
    except HttpError as e:
        return False, e

def delete_calendar(cal_id):
    global service
    service.calendars().delete(calendarId=cal_id).execute()

def get_primary_calendar_id():
    return get_calendar_info('primary')['id']

def delete_event(event_id):
    global service
    service.events().delete(calendarId='primary', eventId=event_id).execute()

def auth_setup():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    global service
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

def APILookup(desc, *args, **kw):
    py = []
    http = "Not set"
    py.append("service = build('calendar', 'v3', credentials=creds)")
    if (desc == 'Event List'):
        http = 'GET https://www.googleapis.com/calendar/v3/calendars/primary/events?maxResults=10&orderBy=startTime&singleEvents=true&timeMin=[now]&key=[YOUR_API_KEY]'
        py.append("events_result = service.events().list(calendarId='primary', timeMin=[now], maxResults=10, singleEvents=True, orderBy='startTime').execute()")
        py.append("events = events_result.get('items', [])")
        return http, py

    elif (desc == 'Event Get'):
        http = 'GET https://www.googleapis.com/calendar/v3/calendars/primary/events/[eventId]&key=[YOUR_API_KEY]'
        py.append("event_info = service.events().get(calendarId='primary', eventId=[eventId]).execute()")

    elif (desc == 'Event Delete'):
        http = 'DELETE https://www.googleapis.com/calendar/v3/calendars/primary/events/[eventId]?&key=[YOUR_API_KEY]'
        py.append("service.events().delete(calendarId='primary', eventId=event_id).execute()")

    elif (desc == 'Event Insert'):
        event_data = create_event_from_data()
        http = f"POST https://www.googleapis.com/calendar/v3/calendars/primary/events?key=[YOUR_API_KEY]\n{event_data}"
        py.append("service.events().insert(calendarId='primary', body=event_data).execute()")

    elif (desc == 'Calendar List'):
        http = 'GET https://www.googleapis.com/calendar/v3/users/me/calendarList?key=[YOUR_API_KEY]'
        py.append('cals = service.calendarList().list(maxResults=num_results).execute()')
        py.append("cals = cals.get('items', [])")

    elif (desc == 'Calendar Get'):
        http = 'GET https://www.googleapis.com/calendar/v3/calendars/[calendarId]?key=[YOUR_API_KEY]'
        py.append("cal_info = service.calendars().get(calendarId=cal_id).execute()")

    elif (desc == 'Calendar Insert'):
        calendar_data = create_calendar()
        http = f"POST https://www.googleapis.com/calendar/v3/calendars?key=[YOUR_API_KEY]\n{calendar_data}"
        py.append("service.calendars().insert(body=cal_data).execute()")

    elif (desc == 'Calendar Delete'):
        http = 'DELETE https://www.googleapis.com/calendar/v3/calendars/[calendarId]?key=[YOUR_API_KEY]'
        py.append("service.calendars().delete(calendarId=cal_id).execute()")

    else:
        http = ''
        py = ''

    return http, py