# Moving Average Calculation for Delivery Times

## Requirements

Python 3.x
Required Python packages: json, datetime

## Usage

1.	Input File: Place your JSON file containing events (events.json) in the same directory as the script.

2.	Running the Script:
		unbabel_cli.py --input_file events.json --window_size 10

3.	Output: The script prints the moving average delivery times to the console, formatted as JSON objects with timestamps and average delivery times.

## Description

IIn the first place, the current time is read and the start timestamp based on the window size is calculated. After, the events.json file is open and the events are read and filtered according to the specified time range. If this file is empty or does not exist, it throws an error. 

Once we have the filtered events, its calculated the moving averages. To iterate the filtered events, it's used a variable ("index") to track the index of the next event that will be processed.  Since these events are ordered by the timestamp key, from lower (oldest) to higher values, it means after we find an event with the timestamp for the minute we are searching for, once we go to the next minute in the loop, we don't need to search in all the filtered events for a possible correspondence, we know the next value will be in the position of the value stored in the variable "index".  The results are stored in a list called "moving_averages".

If there are no events that fall within the specific time range, the average for all minutes will be considered zero. 
