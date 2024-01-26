#!/usr/bin/env python
# coding: utf-8

# In[29]:


import csv
from datetime import datetime, timedelta

def parse_time(time_str):
   
    if time_str:
        return datetime.strptime(time_str, "%m/%d/%Y %I:%M %p")
    else:
        return None

def convert_time_to_minutes(time_str):
    
    if time_str:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    else:
        return 0

def analyze_file(file_path):
  
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                employee_name = row['Employee Name']
                position = row['Position ID']
                time_in = parse_time(row['Time'])
                time_out = parse_time(row['Time Out'])
                timecard_hours_str = row['Timecard Hours (as Time)']

                if time_in is None or time_out is None:
                    continue  
                timecard_minutes = convert_time_to_minutes(timecard_hours_str)

              
                consecutive_days = 1
                for next_row in reader:
                    next_time_in = parse_time(next_row['Time'])
                    if next_time_in and (next_time_in - time_out).days == 1:
                        consecutive_days += 1
                        time_out = parse_time(next_row['Time Out'])
                    else:
                        break
                if consecutive_days == 7:
                    print(f"{employee_name} ({position}) has worked for 7 consecutive days.")

                if next_time_in:
                    time_between_shifts = (next_time_in - time_out).seconds / 3600
                    if 1 < time_between_shifts < 10:
                        print(f"{employee_name} ({position}) has less than 10 hours between shifts.")

                if timecard_minutes > 14 * 60:
                    print(f"{employee_name} ({position}) has worked for more than 14 hours in a single shift.")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = r'C:\Users\91626\Downloads\Assignement.csv.csv'
analyze_file(file_path)


# In[ ]:




