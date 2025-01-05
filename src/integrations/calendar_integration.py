from datetime import datetime
from typing import Dict, List, Optional
import requests

class CalendarIntegration:
    def __init__(self, api_key: str, calendar_service: str = "google"):
        self.api_key = api_key
        self.calendar_service = calendar_service
        self.base_url = self._get_service_url()
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _get_service_url(self) -> str:
        """Get the appropriate API URL for the calendar service."""
        services = {
            "google": "https://www.googleapis.com/calendar/v3",
            "outlook": "https://graph.microsoft.com/v1.0/me/calendar"
        }
        return services.get(self.calendar_service, services["google"])

    def create_event(self, event_data: Dict) -> Optional[Dict]:
        """Create a calendar event from meeting summary data."""
        try:
            endpoint = f"{self.base_url}/events"
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=event_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error creating calendar event: {str(e)}")
            return None

    def create_followup_meeting(self, summary: str, start_time: datetime, duration_minutes: int = 30, attendees: List[str] = None) -> Optional[Dict]:
        """Create a follow-up meeting based on action items."""
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        event_data = {
            "summary": f"Follow-up: {summary}",
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC"
            },
            "attendees": [{"email": attendee} for attendee in (attendees or [])]
        }
        
        return self.create_event(event_data)