import time
import datetime

# Function to read and process data from a given file
def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) > 1:
                try:
                    # Extract relevant columns
                    num_passengers = int(parts[3])
                    fare_amount = float(parts[10])
                    total_amount = float(parts[16])
                    trip_distance = float(parts[4])
                    pickup = parts[1]
                    dropoff = parts[2]

                    # Convert pickup/dropoff times into seconds
                    time_format = "%Y-%m-%dT%H:%M:%S.%f"
                    pickup_time = time.strptime(pickup, time_format)
                    dropoff_time = time.strptime(dropoff, time_format)
                    trip_time_seconds = time.mktime(
                        dropoff_time) - time.mktime(pickup_time)

                    if trip_time_seconds > 0:  # Avoid dividing by zero
                        speed = trip_distance / (trip_time_seconds / 3600
                                                 )  # speed in mph
                        data.append((num_passengers, fare_amount, total_amount,
                                     speed, trip_time_seconds))
                except ValueError:
                    continue  # Skip lines with junk data
    return data


# Bubble sort implementation for sorting data based on a specific key index
def bubble_sort(data, key_index):
    data = data[:]  # Make a copy to avoid modifying the original list
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j][key_index] > data[j + 1][key_index]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


# Merge sort implementation for sorting data based on a specific key index
def merge_sort(data, key_index):
    if len(data) > 1:
        mid = len(data) // 2  # Find the middle point
        left_half = merge_sort(data[:mid], key_index)
        right_half = merge_sort(data[mid:], key_index)

        data = []
        # Merge the two halves back together in sorted order
        while len(left_half) > 0 and len(right_half) > 0:
            if left_half[0][key_index] < right_half[0][key_index]:
                data.append(left_half.pop(0))
            else:
                data.append(right_half.pop(0))
        data.extend(left_half)
        data.extend(right_half)
    return data


# Function to measure the performance of bubble sort and merge sort
def measure_sorting_algorithms(data):
    start_time = time.time()
    sorted_data_bubble = bubble_sort(data, 2)  # Sort by total_amount (index 2)
    bubble_time = time.time() - start_time

    start_time = time.time()
    sorted_data_merge = merge_sort(data, 2)  # Sort by total_amount (index 2)
    merge_time = time.time() - start_time

    return bubble_time, merge_time


# Function to parse each line of the trip data
def parse_trip(line):
    fields = line.split(',')
    try:
        num_passengers = int(fields[3])
        fare_amount = float(fields[10])
        tips_amount = float(fields[14])
        total_amount = float(fields[16])
        pickup_datetime = datetime.datetime.strptime(fields[1],
                                                     "%Y-%m-%d %H:%M:%S")
        dropoff_datetime = datetime.datetime.strptime(fields[2],
                                                      "%Y-%m-%d %H:%M:%S")
        trip_distance = float(fields[4])
        trip_time = (dropoff_datetime -
                     pickup_datetime).total_seconds() / 3600  # hours
        speed = trip_distance / trip_time if trip_time > 0 else 0  # miles per hour
    except ValueError:
        return None  # Skip malformed lines

    return (num_passengers, fare_amount, tips_amount, total_amount, speed,
            trip_time)


# Function to read and parse all trips from the dataset
def read_trips(file_path):
    trips = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the first line, because it's just the header
        for line in file:
            trip = parse_trip(line)
            if trip:
                trips.append(trip)
    return trips


# Quick sort implementation using a key function
def quicksort(data, key_func=lambda x: x):
    if len(data) <= 1:
        return data
    else:
        pivot = data[0]
        lesser = quicksort(
            [x for x in data[1:] if key_func(x) <= key_func(pivot)], key_func)
        greater = quicksort(
            [x for x in data[1:] if key_func(x) > key_func(pivot)], key_func)
        return lesser + [pivot] + greater


# Heap sort implementation using a key function
def heapsort(data, key_func=lambda x: x):
    import heapq
    heap = []
    for value in data:
        heapq.heappush(heap, value)
    return [heapq.heappop(heap) for _ in range(len(heap))]


# Function to measure the performance of any sorting algorithm
def time_sorting_algorithm(algorithm, data, key_func):
    start_time = time.time()
    sorted_data = algorithm(data, key_func)
    end_time = time.time()
    return end_time - start_time, sorted_data


# Load data for all datasets
trips_small = read_trips("nyc_dataset_small.txt")
trips_medium = read_trips("nyc_dataset_medium.txt")
trips_large = read_trips("nyc_dataset_large.txt")

# Measure QuickSort and HeapSort performance for the SMALL dataset
qs_time_small, qs_sorted_small = time_sorting_algorithm(
    quicksort, trips_small, key_func=lambda x: x[3])  # Sort by total_amount
hs_time_small, hs_sorted_small = time_sorting_algorithm(
    heapsort, trips_small, key_func=lambda x: x[3])  # Sort by total_amount

# Measure QuickSort and HeapSort performance for the MEDIUM dataset
qs_time_medium, qs_sorted_medium = time_sorting_algorithm(
    quicksort, trips_medium, key_func=lambda x: x[3])  # Sort by total_amount
hs_time_medium, hs_sorted_medium = time_sorting_algorithm(
    heapsort, trips_small, key_func=lambda x: x[3])  # Sort by total_amount

# Measure QuickSort and HeapSort performance for the LARGE dataset
qs_time_large, qs_sorted_large = time_sorting_algorithm(
    quicksort, trips_large, key_func=lambda x: x[3])  # Sort by total_amount
hs_time_large, hs_sorted_large = time_sorting_algorithm(
    heapsort, trips_small, key_func=lambda x: x[3])  # Sort by total_amount

# Load data and measure Bubble Sort and Merge Sort performance
data_small = read_data('nyc_dataset_small.txt')
data_medium = read_data('nyc_dataset_medium.txt')
data_large = read_data('nyc_dataset_large.txt')

bubble_time_small, merge_time_small = measure_sorting_algorithms(data_small)
bubble_time_medium, merge_time_medium = measure_sorting_algorithms(data_medium)
bubble_time_large, merge_time_large = measure_sorting_algorithms(data_large)

# Print results for the SMALL dataset
print(f"Bubble Sort Time: {bubble_time_small} seconds")
print(f"Merge Sort Time: {merge_time_small} seconds")
print(f"QuickSort Time: {qs_time_small} seconds")
print(f"HeapSort Time: {hs_time_small} seconds")

# Print results for the MEDIUM dataset
print(f"Bubble Sort Time: {bubble_time_medium} seconds")
print(f"Merge Sort Time: {merge_time_medium} seconds")
print(f"QuickSort Time: {qs_time_medium} seconds")
print(f"HeapSort Time: {hs_time_medium} seconds")

# Print results for the LARGE dataset
print(f"Bubble Sort Time: {bubble_time_large} seconds")
print(f"Merge Sort Time: {merge_time_large} seconds")
print(f"QuickSort Time: {qs_time_large} seconds")
print(f"HeapSort Time: {hs_time_large} seconds")
