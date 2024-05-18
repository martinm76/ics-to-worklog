# ics-to-worklog
A simple Python script to generate a worklog from an ics (iCalendar) file. First version generated purely through prompting GPT-4o, roughly 10 generations

# ICS to Worklog Converter

## Purpose

This script converts `.ics` calendar files into worklogs. The worklog format includes the start time, end time, title, location, and description of each event. It also handles recurring events, filters events by date range, and excludes declined events. Each day's events are summarized with a header, and the total time spent on events for each day is calculated and displayed.

## Features

- Handles recurring events.
- Excludes declined events.
- Filters events by specified date range.
- Formats event descriptions to remove extraneous information.
- Adds headers and separators for better readability.
- Calculates and displays total time spent on events for each day.

## Dependencies

- Python 3.x
- ics (>= 0.7)
- pytz (>= 2021.1)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/martinm76/ics-to-worklog.git
    cd ics-to-worklog
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, you can install the dependencies manually:

    ```bash
    pip install ics pytz
    ```

## Usage

To convert an `.ics` file to a worklog, run the script with the following command:

```bash
python ics_to_worklog.py path_to_your_file.ics --startdate YYYY-MM-DD --enddate YYYY-MM-DD
