from pathlib import Path
import re
import dateparser
import json


class Event:
    def __init__(self, text, date, club):
        self.text = text
        self.date = date
        self.club = club


def get_date(text, months):
    for month in months:
        regex = rf"(\d{{1,2}})\s({month})|({month})\s(\d{{1,2}})|(\d{{1,2}})..\s({month})"
        match = re.search(regex, text)

        if match:
            if match.group(1):
                day = match.group(1)
                month = match.group(2)
            elif match.group(3):
                month = match.group(3)
                day = match.group(4)
            else:
                day = match.group(5)
                month = match.group(6)
            string_date = month + " " + day
            return dateparser.parse(string_date)

    return None


months = [
    "Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec",
    "January", "February", "March", "April", "August", "September", "October", "November", "December"
]
events = []

# Cross-platform path (works on Windows locally and Linux on GitHub Actions)
folder_path = Path("gallery-dl") / "instagram"

if not folder_path.exists():
    print(f"Folder not found: {folder_path}. Has the scraper been run yet?")
else:
    for file_path in folder_path.rglob("*.txt"):
        try:
            with file_path.open("r", encoding="utf-8") as file:
                content = file.read()

            date = get_date(content, months)

            if not date:
                print(f"No date found, deleting: {file_path}")
                file_path.unlink()
            else:
                print(f"Found date: {date} | File: {file_path}")
                event = Event(content, date, file_path.parent.name)
                events.append(event)

        except Exception as e:
            print(f"Could not process {file_path}: {e}")

print(f"Found {len(events)} events total.")

# Deduplicate: keep longest description per (club, date) pair
unique_events = {}
for event in events:
    key = (event.club, event.date)
    if key not in unique_events or len(event.text) > len(unique_events[key].text):
        unique_events[key] = event

events = list(unique_events.values())

# Sort by date ascending
events.sort(key=lambda e: e.date)

event_data = []
for event in events:
    event_data.append({
        "club": event.club,
        "date": event.date.strftime("%Y-%m-%d"),
        "description": event.text
    })

with open("events.json", "w", encoding="utf-8") as f:
    json.dump(event_data, f, indent=4, ensure_ascii=False)

print(f"Written {len(event_data)} events to events.json.")
