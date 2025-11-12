from datetime import datetime, timedelta
from ics import Calendar, Event

def create_ics_event(summary: str, days_from_now: int = 2, duration_minutes: int = 30):
    """Generate a .ics calendar file for follow-up."""
    cal = Calendar()
    event = Event()
    event.name = summary
    event.begin = datetime.now() + timedelta(days=days_from_now)
    event.duration = {"minutes": duration_minutes}
    cal.events.add(event)

    filename = f"followup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"
    with open(filename, "w") as f:
        f.writelines(cal)
    return filename
