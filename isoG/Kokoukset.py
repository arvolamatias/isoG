import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import datetime
import json


with open('result_27_10_2023.json', 'rb') as f:
    raw_data = f.read()

data = json.loads(raw_data)

# find meetings and group by date timestamp YYYY-MM-DD
keywords = ['kokous', 'gokous', 'avaus',
            'meeting', 'gogous', 'opening', 'kokouksen', 'puheenjohtaja', 'sihteeri', 'laillisuus', 'ajassa','uusien','support','legality'
            ,'closing','ilmoitusasiat','pöytäkirja']
meetings = {}
meetingCount = 0
mostMeetingsPerDay = 0
mostMeetingsDate = ''
mostMeetinsgWeekday = ''

for msg in data['messages']:
    if len(msg['text']) > 100 and any(keyword in msg['text'] for keyword in keywords):
        date = msg['date'].split('T')[0]
        if date in meetings:
            meetings[date].append(msg)
        else:
            meetings[date] = [msg]

# Calculate the number of meetings for each year, weekday, and month
yearly_meetings = {}
weekday_meetings = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
monthly_meetings = {str(i).zfill(2): 0 for i in range(1, 13)}  # Padded with leading zeros
time_of_day_meetings = {f"{i:02}:00-{(i + 1) % 24:02}:00": 0 for i in range(24)}

for msg in data['messages']:
    if len(msg['text']) > 100 and any(keyword in msg['text'] for keyword in keywords):
        date = msg['date'].split('T')[0]
        year = date.split('-')[0]

        # Initialize the year key if it doesn't exist
        if year not in yearly_meetings:
            yearly_meetings[year] = 0

        # Update the count for the year
        yearly_meetings[year] += 1

        time = msg['date'].split('T')[1].split(':')[0]  # Extract the hour from the timestamp

        # Calculate the 1-hour time section based on the hour in the timestamp
        time_section = f"{int(time):02}:00-{(int(time) + 1) % 24:02}:00"

        # Initialize the time_section key if it doesn't exist
        if time_section not in time_of_day_meetings:
            time_of_day_meetings[time_section] = 0

        # Update the count for the time section
        time_of_day_meetings[time_section] += 1

        # Update data dictionaries
        if date in meetings:
            meetings[date].append(msg)
        else:
            meetings[date] = [msg]

        weekday = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        weekday_meetings[weekday] += 1

        month = date.split('-')[1]
        monthly_meetings[month] += 1
        time_of_day_meetings[time_section] += 1

# Interactive user input to select filtering option
print("Select filtering option:")
print("1. Show number of meetings for each year")
print("2. Show number of meetings for each weekday")
print("3. Show number of meetings for each month")
print("4. Show number of meetings for each hour of the day")
option = input("Enter 1, 2, 3, or 4: ")

if option == '1':
    years = list(yearly_meetings.keys())
    meeting_counts = [yearly_meetings[year] for year in years]
    x_label = 'Year'
    y_label = 'Number of Meetings per Year'
elif option == '2':
    years = list(weekday_meetings.keys())
    meeting_counts = list(weekday_meetings.values())
    x_label = 'Weekday'
    y_label = 'Number of Meetings per Weekday'
elif option == '3':
    years = [f"Month {i}" for i in range(1, 13)]
    meeting_counts = list(monthly_meetings.values())
    x_label = 'Month'
    y_label = 'Number of Meetings per Month'
elif option == '4':
    years = list(time_of_day_meetings.keys())
    meeting_counts = list(time_of_day_meetings.values())
    x_label = 'Time of Day'
    y_label = 'Number of Meetings per Hour'
else:
    print("Invalid option. Please enter 1, 2, 3, or 4.")
    exit()

# Create a bar chart to visualize the filtered data
plt.bar(years, meeting_counts, color='b')
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(f'Number of Meetings {y_label}')
plt.xticks(rotation=45)

for i in range(len(years)):
    plt.text(years[i], meeting_counts[i], str(meeting_counts[i]), ha='center', va='bottom')
        
plt.show()



