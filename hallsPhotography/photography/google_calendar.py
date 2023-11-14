import googleapiclient.discovery
from google.oauth2 import service_account
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the JSON file
json_file_path = os.path.join(script_dir, 'halls-photography-1c12a0d9b677.json')

# Load the credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(
    json_file_path,
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)

# Load the crjj
start_time = '2020-01-14T01:25:06.172124Z'
end_time = '2024-12-21T01:25:06.172124Z' 


# Build the service using the credentials.
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
def get_google_calendar_events(start_time, end_time):
    # List both events and potential tasks from the primary calendar.
    events_and_tasks = service.events().list(
        calendarId='stefhall.2704@gmail.com',
        timeMin=start_time,
        timeMax=end_time,
        alt='json'
    ).execute()
    # Print the events and potential tasks to the console.
    event_detail = dict()
    return events_and_tasks.get("items", [])
