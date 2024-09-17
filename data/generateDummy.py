import pandas as pd
import datetime
import random

# Define the approximate boundaries of the Indian Ocean
min_lat = -40
max_lat = 30
min_lon = 20
max_lon = 100

# Define the time range for the data
start_time = datetime.datetime(2023, 1, 1)
end_time = datetime.datetime(2024, 8, 31)

# Initialize an empty list to hold the data
data = []

# Store used coordinates to avoid duplicates
used_coordinates = set()

# Generate waypoints with a 0.5 degree interval, avoiding landmasses and duplicates
latitude = min_lat
while latitude <= max_lat:
    longitude = min_lon
    while longitude <= max_lon:
        coordinate_string = f"{latitude},{longitude}"
        if coordinate_string not in used_coordinates:
            elevation = 0  # Assuming sea level
            timestamp = start_time + \
                datetime.timedelta(seconds=random.randint(
                    0, int((end_time - start_time).total_seconds())))

            # Append data to the list
            data.append([latitude, longitude, elevation,
                        timestamp.strftime('%Y-%m-%d %H:%M:%S')])
            used_coordinates.add(coordinate_string)
        longitude += 1.8
    latitude += 1.8

# Create a DataFrame
df = pd.DataFrame(
    data, columns=['latitude', 'longitude', 'elevation', 'timestamp'])

# Export the DataFrame to a CSV file
df.to_csv('data\\dummy_waypoints.csv', index=False)
