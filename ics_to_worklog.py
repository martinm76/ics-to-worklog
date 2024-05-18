import argparse
from ics import Calendar
from datetime import datetime, timedelta
import pytz

def format_event(event):
    start = event.begin.to('local').strftime('%H:%M')
    end = event.end.to('local').strftime('%H:%M')
    title = event.name
    location = f" [{event.location}]" if event.location else ""
    description = event.description or ""  # Ensure description is an empty string if None
    if description:
        # Remove everything from the first occurrence of '-::' to the end
        description = description.split('-::')[0]
        description = f" ({description.strip()})" if description.strip() else ""
    return f"{start} - {end} : {title}{location}{description}"

def calculate_time_spent(events):
    total_duration = timedelta()
    for event in events:
        total_duration += event.end - event.begin
    return total_duration

def convert_ics_to_worklog(file_path, start_date, end_date):
    with open(file_path, 'r') as file:
        calendar = Calendar(file.read())
    
    events = []
    for event in calendar.timeline:
        # Skip declined events
        if event.status == 'DECLINED':
            continue
        event_start = event.begin.datetime
        if start_date <= event_start <= end_date:
            events.append(event)

    # Sort events by start time
    events.sort(key=lambda e: e.begin)

    worklog = []
    current_day = None
    daily_events = []
    
    for event in events:
        event_day = event.begin.date()
        if current_day is None or event_day != current_day:
            if daily_events:
                # Sum up the time spent for the current day
                total_time = calculate_time_spent(daily_events)
                worklog.append("-" * 30)
                worklog.append(f"Total time spent: {total_time}")
                worklog.append("")  # Add an empty line for separation
            current_day = event_day
            daily_events = []
            # Add header for the new day
            day_header = f"{current_day.isoformat()} ({current_day.strftime('%A')})"
            worklog.append(day_header)
            worklog.append("=" * 30)
        daily_events.append(event)
        worklog.append(format_event(event))
    
    if daily_events:
        # Sum up the time spent for the last day
        total_time = calculate_time_spent(daily_events)
        worklog.append("-" * 30)
        worklog.append(f"Total time spent: {total_time}")

    return "\n".join(worklog)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert .ics calendar files to worklogs.')
    parser.add_argument('file', help='Path to the .ics file')
    parser.add_argument('--startdate', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--enddate', required=True, help='End date in YYYY-MM-DD format')
    args = parser.parse_args()

    # Parse dates and make them timezone-aware
    start_date = pytz.utc.localize(datetime.strptime(args.startdate, '%Y-%m-%d'))
    end_date = pytz.utc.localize(datetime.strptime(args.enddate, '%Y-%m-%d')) + timedelta(days=1) - timedelta(seconds=1)

    worklog = convert_ics_to_worklog(args.file, start_date, end_date)
    print(worklog)

