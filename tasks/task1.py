from typing import List, Dict, Tuple
from datetime import datetime

# Function to read CSV file into a list of dictionaries
def read_file(file_path: str) -> List[Dict[str, any]]:
    """Reads a CSV file and returns a list of dictionaries representing the data."""
    data = []
    with open(file_path, 'r') as file:
        headers = file.readline().strip().split(',')  # Extract column headers
        for line in file:
            values = line.strip().split(',')
            # Create a dictionary for each line with column headers as keys
            entry = {headers[i]: values[i] for i in range(len(values))}
            data.append(entry)
    return data

# Function to calculate statistics
def calculate_stats(data: List[Dict[str, any]]) -> Dict[str, Tuple[float, float, float]]:
    """Calculates minimum, average, and maximum values for given columns."""
    def calc_stats(values: List[float]) -> Tuple[float, float, float]:
        """Helper function to calculate min, avg, max of a list of values."""
        if values:
            return min(values), sum(values) / len(values), max(values)
        else:
            return 0.0, 0.0, 0.0

    # Extract relevant columns and filter out invalid values
    total_amounts = [float(trip['total_amount']) for trip in data if trip['total_amount'] and trip['total_amount'] != '' and float(trip['total_amount']) > 0]
    tip_amounts = [float(trip['tip_amount']) for trip in data if trip['tip_amount'] and trip['tip_amount'] != '' and float(trip['tip_amount']) >= 0]

    # Return statistics for total and tip amounts
    return {
        'total_amount': calc_stats(total_amounts),
        'tip_amount': calc_stats(tip_amounts)
    }

# Function to calculate speed statistics
def calculate_speed(data: List[Dict[str, any]]) -> Tuple[float, float, float]:
    """Calculates speed statistics (min, avg, max) from taxi trip data."""
    speeds = []
    for trip in data:
        if 'tpep_pickup_datetime' in trip and 'tpep_dropoff_datetime' in trip and 'trip_distance' in trip:
            try:
                # Parse datetime and trip distance values
                pickup_time = datetime.strptime(trip['tpep_pickup_datetime'], '%Y-%m-%dT%H:%M:%S.%f')
                dropoff_time = datetime.strptime(trip['tpep_dropoff_datetime'], '%Y-%m-%dT%H:%M:%S.%f')
                distance = float(trip['trip_distance']) * 1.60934  # Convert miles to km
                duration_hours = (dropoff_time - pickup_time).total_seconds() / 3600  # Convert to hours

                # Calculate speed in km/h
                if duration_hours > 0 and distance > 0:
                    speed_kmh = distance / duration_hours
                    speeds.append(speed_kmh)
            except ValueError:
                continue  # Skip lines with invalid data

    # Filter out unrealistic speeds
    if speeds:
        realistic_speeds = [speed for speed in speeds if 0 < speed <= 150]  # Assuming realistic speed limits
        if realistic_speeds:
            return min(realistic_speeds), sum(realistic_speeds) / len(realistic_speeds), max(realistic_speeds)
        else:
            return 0.0, 0.0, 0.0
    return 0.0, 0.0, 0.0

# Function to read taxi zone lookup table
def read_zone_lookup(file_path: str) -> Dict[int, str]:
    """Reads a taxi zone lookup file and returns a dictionary mapping IDs to zone names."""
    zones = {}
    with open(file_path, 'r') as file:
        next(file)  # Skip the header
        for line in file:
            parts = line.strip().split(',')
            location_id = int(parts[0].strip('"'))
            zone_name = parts[2].strip('"')
            zones[location_id] = zone_name
    return zones

# Function to count trips per zone
def count_trips(data: List[Dict[str, any]], zones: Dict[int, str]) -> Dict[str, int]:
    """Counts the number of trips for each specified zone."""
    # Initialize a dictionary to hold counts for each zone
    zone_counts = {zone_name: 0 for zone_name in zones.values()}

    # Increment counts based on pickup location
    for trip in data:
        try:
            zone_id = int(trip['PULocationID'])
            if zone_id in zones:
                zone_name = zones[zone_id]
                zone_counts[zone_name] += 1
        except Exception as e:
            continue  # Skip lines with invalid data
    return zone_counts

# Read all the data and zone lookup file paths
data_path_small = 'nyc_dataset_small.txt'
data_path_medium = 'nyc_dataset_medium.txt'
data_path_large = 'nyc_dataset_large.txt'
zone_lookup_path = 'taxi+_zone_lookup.csv'

# Load taxi trip data for all datasets
data_small = read_file(data_path_small)
data_medium = read_file(data_path_medium)
data_large = read_file(data_path_large)

# Calculate statistics for total amount and tip amount for all datasets
stats_small = calculate_stats(data_small)
stats_medium = calculate_stats(data_medium)
stats_large = calculate_stats(data_large)

total_amount_stats_small = stats_small['total_amount']
tip_amount_stats_small = stats_small['tip_amount']

total_amount_stats_medium = stats_medium['total_amount']
tip_amount_stats_medium = stats_medium['tip_amount']

total_amount_stats_large = stats_large['total_amount']
tip_amount_stats_large = stats_large['tip_amount']

# Calculate speed statistics for all datasets
min_speed_small, avg_speed_small, max_speed_small = calculate_speed(data_small)
min_speed_medium, avg_speed_medium, max_speed_medium = calculate_speed(data_medium)
min_speed_large, avg_speed_large, max_speed_large = calculate_speed(data_large)

# Load the zone lookup data from the CSV
zones = read_zone_lookup(zone_lookup_path)

# Filter zones of interest
zones_of_interest = {id: name for id, name in zones.items() if name in 
                     ["Newark Airport", "JFK Airport", "East Harlem North", "Central Park"]
                     }

# Count the number of trips for each zone
trip_counts_small = count_trips(data_small, zones_of_interest)
trip_counts_medium = count_trips(data_medium, zones_of_interest)
trip_counts_large = count_trips(data_large, zones_of_interest)

# Output the results in the desired format - SMALL
print(f"1) Minimum Total Amount: ${total_amount_stats_small[0]}, Average Total Amount: ${total_amount_stats_small[1]:.2f}, Maximum Total Amount: ${total_amount_stats_small[2]}")
print(f"2) Minimum Tip Amount: ${tip_amount_stats_small[0]}, Average Tip Amount: ${tip_amount_stats_small[1]:.2f}, Maximum Tip Amount: ${tip_amount_stats_small[2]}")
print(f"3) {', '.join([f'{zone}: {count}' for zone, count in trip_counts_small.items()])}")

# Output the results in the desired format - MEDIUM
print(f"1) Minimum Total Amount: ${total_amount_stats_medium[0]}, Average Total Amount: ${total_amount_stats_medium[1]:.2f}, Maximum Total Amount: ${total_amount_stats_medium[2]}")
print(f"2) Minimum Tip Amount: ${tip_amount_stats_medium[0]}, Average Tip Amount: ${tip_amount_stats_medium[1]:.2f}, Maximum Tip Amount: ${tip_amount_stats_medium[2]}")
print(f"3) {', '.join([f'{zone}: {count}' for zone, count in trip_counts_medium.items()])}")

# Output the results in the desired format - LARGE
print(f"1) Minimum Total Amount: ${total_amount_stats_large[0]}, Average Total Amount: ${total_amount_stats_large[1]:.2f}, Maximum Total Amount: ${total_amount_stats_large[2]}")
print(f"2) Minimum Tip Amount: ${tip_amount_stats_large[0]}, Average Tip Amount: ${tip_amount_stats_large[1]:.2f}, Maximum Tip Amount: ${tip_amount_stats_large[2]}")
print(f"3) {', '.join([f'{zone}: {count}' for zone, count in trip_counts_large.items()])}")
