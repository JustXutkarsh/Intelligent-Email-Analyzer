# utils/google_calendar.py
import os
import pickle
from datetime import datetime, timedelta
from dateutil import parser as dateparser
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope for calendar events
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

TOKEN_PATH = "token.json"
CLIENT_SECRETS_FILE = "client_secrets.json"

def do_local_oauth():
    """
    Runs an installed-app OAuth flow in the local browser and stores credentials in token.json.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    # Save credentials
    with open(TOKEN_PATH, "wb") as f:
        pickle.dump(creds, f)
    return creds

def load_credentials():
    """
    Loads saved credentials if available, otherwise returns None.
    """
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as f:
            creds = pickle.load(f)
        # If expired/invalid, user should re-run do_local_oauth
        if getattr(creds, "expired", False) and getattr(creds, "refresh_token", None):
            try:
                creds.refresh(Request())
            except Exception:
                return None
        return creds
    return None

def create_event(summary: str, description: str = "", start_dt: datetime = None, duration_minutes: int = 30):
    """
    Create a Google Calendar event using saved credentials (or raises if not authorized).
    start_dt should be a timezone-aware or naive datetime (treated as local).
    Returns the created event resource.
    """
    creds = load_credentials()
    if creds is None:
        raise RuntimeError("No Google credentials found. Please authenticate first (do_local_oauth).")

    service = build("calendar", "v3", credentials=creds)
    if start_dt is None:
        start_dt = datetime.now() + timedelta(days=2)

    # Convert datetimes to RFC3339 strings
    start_iso = start_dt.isoformat()
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    end_iso = end_dt.isoformat()

    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_iso},
        "end": {"dateTime": end_iso},
    }
    created = service.events().insert(calendarId="primary", body=event).execute()
    return created

# --- Utility to parse a suggested_timeframe string into a datetime ---
import re
import calendar

WEEKDAYS = {d.lower(): i for i, d in enumerate(calendar.day_name)}  # monday=0

def parse_timeframe_to_datetime(suggested: str):
    """
    Heuristic parser:
    - "in 2 days" -> today + 2 days
    - "2 days" -> today + 2 days
    - "by Friday" -> next Friday (this week or next)
    - "next week" -> 7 days from now
    - fallback -> 2 days from now
    """
    s = (suggested or "").strip().lower()
    now = datetime.now()

    # direct "in N days" or "N days"
    m = re.search(r"(\d+)\s*day", s)
    if m:
        days = int(m.group(1))
        return now + timedelta(days=days)

    # "by <weekday>"
    m = re.search(r"by\s+([a-zA-Z]+)", s)
    if m:
        wd = m.group(1).lower()
        if wd in WEEKDAYS:
            target = WEEKDAYS[wd]
            today_wd = now.weekday()
            days_ahead = (target - today_wd) % 7
            if days_ahead == 0:
                days_ahead = 7  # schedule next week if same day
            return now + timedelta(days=days_ahead)

    if "next week" in s:
        return now + timedelta(days=7)

    # fallback: in 2 days
    return now + timedelta(days=2)
