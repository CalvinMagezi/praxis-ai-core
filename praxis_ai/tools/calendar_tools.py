# tools/calendar_tools.py

import ell
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import datetime
from ..config.settings import GOOGLE_CALENDAR_CREDENTIALS_FILE

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CALENDAR_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

@ell.tool()
def schedule_meeting(title: str, description: str, start_time: str, end_time: str, attendees: str):
    """
    Schedule a meeting on Google Calendar.
    
    Args:
    title (str): The title of the meeting.
    description (str): A description of the meeting.
    start_time (str): The start time of the meeting in ISO format (e.g., '2023-06-01T09:00:00-07:00').
    end_time (str): The end time of the meeting in ISO format (e.g., '2023-06-01T10:00:00-07:00').
    attendees (str): Comma-separated list of attendee email addresses.
    
    Returns:
    str: A message indicating the result of the scheduling attempt.
    """
    try:
        service = get_calendar_service()
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [{'email': attendee.strip()} for attendee in attendees.split(',')],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Meeting scheduled successfully. Event ID: {event.get('id')}"
    except HttpError as error:
        return f"An error occurred: {error}"

@ell.tool()
def list_upcoming_meetings(max_results: int = 10):
    """
    List upcoming meetings from Google Calendar.
    
    Args:
    max_results (int): Maximum number of meetings to retrieve (default: 10).
    
    Returns:
    str: A formatted list of upcoming meetings.
    """
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=max_results, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return "No upcoming events found."
        
        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_list.append(f"- {start}: {event['summary']}")
        
        return "Upcoming events:\n" + "\n".join(event_list)
    except HttpError as error:
        return f"An error occurred: {error}"