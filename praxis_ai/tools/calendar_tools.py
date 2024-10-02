# tools/calendar_tools.py

import ell
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import datetime
import pytz
from ..config.settings import GOOGLE_CALENDAR_CREDENTIALS_FILE, ENABLE_CALENDAR
from rich.console import Console
from rich.prompt import Prompt

console = Console()
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    if not ENABLE_CALENDAR:
        return None

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not GOOGLE_CALENDAR_CREDENTIALS_FILE:
                console.print("[yellow]Google Calendar credentials file path not set.[/yellow]")
                credentials_file = Prompt.ask("Please enter the path to your Google Calendar credentials file")
                os.environ["GOOGLE_CALENDAR_CREDENTIALS_FILE"] = credentials_file
            
            flow = InstalledAppFlow.from_client_secrets_file(
                os.environ["GOOGLE_CALENDAR_CREDENTIALS_FILE"], SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

@ell.tool()
def get_user_timezone():
    """
    Get the user's timezone from Google Calendar settings.
    
    Returns:
    str: The user's timezone (e.g., 'America/Los_Angeles').
    """
    if not ENABLE_CALENDAR:
        return "Calendar functionality is not enabled. Please set ENABLE_CALENDAR=true in your environment or .env file to use this feature."

    try:
        service = get_calendar_service()
        if not service:
            return "Failed to initialize calendar service. Please check your credentials."

        settings = service.settings().get(setting='timezone').execute()
        return settings['value']
    except HttpError as error:
        return f"An error occurred: {error}"

@ell.tool()
def schedule_meeting(title: str, description: str, start_time: str, end_time: str, attendees: str, timezone: str = None):
    """
    Schedule a meeting on Google Calendar.
    
    Args:
    title (str): The title of the meeting.
    description (str): A description of the meeting.
    start_time (str): The start time of the meeting in ISO format (e.g., '2023-06-01T09:00:00').
    end_time (str): The end time of the meeting in ISO format (e.g., '2023-06-01T10:00:00').
    attendees (str): Comma-separated list of attendee email addresses.
    timezone (str, optional): The timezone for the meeting. If not provided, the user's default timezone will be used.
    
    Returns:
    str: A message indicating the result of the scheduling attempt.
    """
    if not ENABLE_CALENDAR:
        return "Calendar functionality is not enabled. Please set ENABLE_CALENDAR=true in your environment or .env file to use this feature."

    try:
        service = get_calendar_service()
        if not service:
            return "Failed to initialize calendar service. Please check your credentials."

        if not timezone:
            timezone = get_user_timezone()

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
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
def list_upcoming_meetings(max_results: int = 10, time_min: str = None, time_max: str = None):
    """
    List upcoming meetings from Google Calendar.
    
    Args:
    max_results (int): Maximum number of meetings to retrieve (default: 10).
    time_min (str, optional): The start of the interval to fetch events from in ISO format.
    time_max (str, optional): The end of the interval to fetch events from in ISO format.
    
    Returns:
    str: A formatted list of upcoming meetings.
    """
    if not ENABLE_CALENDAR:
        return "Calendar functionality is not enabled. Please set ENABLE_CALENDAR=true in your environment or .env file to use this feature."

    try:
        service = get_calendar_service()
        if not service:
            return "Failed to initialize calendar service. Please check your credentials."

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        time_min = time_min or now
        
        events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                              timeMax=time_max,
                                              maxResults=max_results, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return "No upcoming events found."
        
        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            attendees = ', '.join([attendee['email'] for attendee in event.get('attendees', [])])
            event_list.append(f"- {start} to {end}: {event['summary']}\n  Attendees: {attendees}")
        
        return "Upcoming events:\n" + "\n".join(event_list)
    except HttpError as error:
        return f"An error occurred: {error}"

@ell.tool()
def update_meeting(event_id: str, title: str = None, description: str = None, start_time: str = None, end_time: str = None, attendees: str = None, timezone: str = None):
    """
    Update an existing meeting on Google Calendar.
    
    Args:
    event_id (str): The ID of the event to update.
    title (str, optional): The new title of the meeting.
    description (str, optional): The new description of the meeting.
    start_time (str, optional): The new start time of the meeting in ISO format.
    end_time (str, optional): The new end time of the meeting in ISO format.
    attendees (str, optional): Comma-separated list of attendee email addresses.
    timezone (str, optional): The new timezone for the meeting.
    
    Returns:
    str: A message indicating the result of the update attempt.
    """
    if not ENABLE_CALENDAR:
        return "Calendar functionality is not enabled. Please set ENABLE_CALENDAR=true in your environment or .env file to use this feature."

    try:
        service = get_calendar_service()
        if not service:
            return "Failed to initialize calendar service. Please check your credentials."

        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        if title:
            event['summary'] = title
        if description:
            event['description'] = description
        if start_time:
            event['start']['dateTime'] = start_time
        if end_time:
            event['end']['dateTime'] = end_time
        if timezone:
            event['start']['timeZone'] = timezone
            event['end']['timeZone'] = timezone
        if attendees:
            event['attendees'] = [{'email': attendee.strip()} for attendee in attendees.split(',')]

        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        return f"Meeting updated successfully. Event ID: {updated_event['id']}"
    except HttpError as error:
        return f"An error occurred: {error}"

@ell.tool()
def delete_meeting(event_id: str):
    """
    Delete a meeting from Google Calendar.
    
    Args:
    event_id (str): The ID of the event to delete.
    
    Returns:
    str: A message indicating the result of the deletion attempt.
    """
    if not ENABLE_CALENDAR:
        return "Calendar functionality is not enabled. Please set ENABLE_CALENDAR=true in your environment or .env file to use this feature."

    try:
        service = get_calendar_service()
        if not service:
            return "Failed to initialize calendar service. Please check your credentials."

        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return f"Meeting with ID {event_id} deleted successfully."
    except HttpError as error:
        return f"An error occurred: {error}"

@ell.tool()
def find_free_time(duration_minutes: int, start_date: str, end_date: str, timezone: str = None):
    """
    Find available time slots for a meeting of specified duration within a given date range.
    
    Args:
    duration_minutes (int): The duration of the meeting in minutes.
    start_date (str): The start date of the range to search in ISO format (e.g., '2023-06-01').
    end_date (str): The end date of the range to search in ISO format (e.g., '2023-06-07').
    timezone (str, optional): The timezone to use for the search. If not provided, the user's default timezone will be used.
    
    Returns:
    str: A list of available time slots.
    """
    if not ENABLE_CALENDAR:
        return "Calendar functionality is not enabled. Please set ENABLE_CALENDAR=true in your environment or .env file to use this feature."

    try:
        service = get_calendar_service()
        if not service:
            return "Failed to initialize calendar service. Please check your credentials."

        if not timezone:
            timezone = get_user_timezone()

        tz = pytz.timezone(timezone)
        start_datetime = tz.localize(datetime.datetime.fromisoformat(start_date))
        end_datetime = tz.localize(datetime.datetime.fromisoformat(end_date))

        body = {
            "timeMin": start_datetime.isoformat(),
            "timeMax": end_datetime.isoformat(),
            "timeZone": timezone,
            "items": [{"id": "primary"}]
        }

        free_busy_request = service.freebusy().query(body=body).execute()
        busy_slots = free_busy_request[u'calendars'][u'primary'][u'busy']

        available_slots = []
        current_slot = start_datetime

        while current_slot < end_datetime:
            slot_end = current_slot + datetime.timedelta(minutes=duration_minutes)
            if slot_end > end_datetime:
                break

            is_free = True
            for busy in busy_slots:
                busy_start = datetime.datetime.fromisoformat(busy['start'].rstrip('Z'))
                busy_end = datetime.datetime.fromisoformat(busy['end'].rstrip('Z'))
                if (current_slot < busy_end) and (slot_end > busy_start):
                    is_free = False
                    current_slot = busy_end
                    break

            if is_free:
                available_slots.append(f"{current_slot.isoformat()} - {slot_end.isoformat()}")
                current_slot = slot_end
            else:
                current_slot += datetime.timedelta(minutes=15)

        if available_slots:
            return "Available time slots:\n" + "\n".join(available_slots)
        else:
            return "No available time slots found in the specified range."
    except HttpError as error:
        return f"An error occurred: {error}"