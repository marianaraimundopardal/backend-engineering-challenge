import json
from datetime import datetime, timedelta
import argparse

#Local tests
#input_file = '/Users/marianarpardal/backend-engineering-challenge/events.json'
#window_size = 5

"""
Calculate moving average of the translation delivery time for each minute within a specified time window

Args:
- input_file (str): Path to the input JSON file containing translation events
- window_size (int): Size of the moving average window in minutes

Returns:
- list: A list with the timestamps and its corresponding moving average delivery time
"""
def get_moving_averages(input_file, window_size):

    # Initialize an empty list to store filtered events that fall within the specified time window
    filtered_events = []

    # Initialize an empty list to store calculated moving averages for each minute within the time window
    moving_averages = []

    # Get the timestamps that will limit the range
    current_timestamp = datetime.now().replace(second=0, microsecond=0)
    start_timestamp = (current_timestamp - timedelta(minutes=window_size)).replace(second=0, microsecond=0)

    # Open and read events.json
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise ValueError("The input file is empty.")
            
            for line in lines:
                # Load JSON object from each line
                json_obj = json.loads(line.strip())
                
                # Get timestamp from JSON object
                timestamp_str = json_obj['timestamp']
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f').replace(second=0, microsecond=0)
                
                # Check if the current timestamp is within the specified range and if it is, append the result to the list
                if start_timestamp <= timestamp <= current_timestamp:
                    filtered_events.append({
                        "timestamp": timestamp,
                        "duration": json_obj['duration']
                    })
                    
                elif timestamp > current_timestamp:
                    break  # Stop processing after reaching the current_timestamp (the end limit)

    except FileNotFoundError:
        raise FileNotFoundError(f"The input file '{input_file}' does not exist.")
    #except Exception as e:
    #    raise Exception(f"An error occurred: {e}")

    # Auxiliar variables used to calculate the moving averages
    aux_timestamp = start_timestamp #for iterating through each minute
    total_sum = 0  # Sum of all durations
    num_events = 0 # Total of events detected in the range
    index = 0 # Value used to track the index of the last processed event in filtered_events
    average = 0 # Average of the event

    # Iterate through each minute within the time window
    while aux_timestamp <= current_timestamp:

        # If this timestamp is the same as the one of the event
        if filtered_events and index < len(filtered_events) and aux_timestamp == filtered_events[index]['timestamp']:
            num_events += 1
            total_sum += filtered_events[index]['duration']
            average = total_sum / num_events
            index += 1
        
        # Append the result to moving_averages list
        moving_averages.append({
            "date": aux_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "average_delivery_time": round(average, 2) 
        })
        
        # Move to the next minute
        aux_timestamp += timedelta(minutes=1)

    return moving_averages

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Calculate moving average delivery time.')
    parser.add_argument('--input_file', required=True, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, required=True, help='Window size in minutes')

    # Parse arguments
    args = parser.parse_args()

    # Call get_moving_averages function with provided arguments
    moving_averages = get_moving_averages(args.input_file, args.window_size)

    # Print the results
    for average in moving_averages:
        print(json.dumps(average))

if __name__ == "__main__":
    main()
