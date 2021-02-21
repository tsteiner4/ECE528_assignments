from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from CalendarApp import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def create_event_from_data(summary="", location="", description="", start="",
                           timeZone="", end="", recurrRule=[],
                           attendees=[], defaultReminder=False, reminderOverrides=[]):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': timeZone,
        },
        'end': {
            'dateTime': end,
            'timeZone': timeZone,
        },
        'recurrence': recurrRule,
        'attendees': attendees,
        'reminders': {
            'useDefault': defaultReminder,
            'overrides': reminderOverrides,
        },
    }
    return event

def get_calendar_events(num_events=10):
    global service
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=num_events, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

def get_event_info(eventId):
    global service
    event_info = service.events().get(calendarId='primary', eventId=eventId).execute()

    return event_info

def add_event(event_data):
    global service
    service.events().insert(calendarId='primary', body=event_data).execute()

def delete_event(event_id):
    global service
    service.events().delete(calendarId='primary', eventId=event_id)

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

    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

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
        py.append("service.events().delete(calendarId='primary', eventId=event_id)")

    elif (desc == 'Event Insert'):
        event_data = create_event_from_data()
        http = f"POST https://www.googleapis.com/calendar/v3/calendars/primary/events?key=[YOUR_API_KEY]\n{event_data}"
        py.append("service.events().insert(calendarId='primary', body=event_data).execute()")

    elif (desc == 'Event Get'):
        http = 'GET https://www.googleapis.com/calendar/v3/calendars/primary/events?key=[YOUR_API_KEY]'

    elif (desc == 'Event Get'):
        http = 'GET https://www.googleapis.com/calendar/v3/calendars/primary/events?key=[YOUR_API_KEY]'
    else:
        http = ''
    return http, py