import threading
import csv
import datetime
import random
import requests


class TimeoutFixed(threading.Thread):
    def __init__(self, function, *args, timeout=6):
        super().__init__()
        self.function = function
        self.args = args
        self.timeout = timeout
        self.result = None
        self.daemon = True  # Ensure thread terminates with main program

    def run(self):
        self.result = self.function(*self.args)

    def join_with_timeout(self):
        self.start()
        self.join(self.timeout)
        if self.is_alive():
            self.result = None  # Indicate timeout occurred


def is_land(latitude, longitude):
    # Use Geoapify's reverse geocoding API to determine if the coordinates are land or water
    api_key = "YOUR_GEOAPIFY_API_KEY"  # Replace with your Geoapify API key
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&apiKey=8c1bf5efead4454da7af0f75a59e9565"
    response = requests.get(url)
    if not response:
        return True
    data = response.json()
    if data.get("features"):
        feature = data["features"][0]["properties"]
        # Check for land or place in result_type
        print(feature)
        if "result_type" in feature and feature["result_type"] in ["unknown"]:
            print(f"{latitude}, {longitude} Checked: Water Body")
            return False

    print(f"{latitude}, {longitude} Checked: Land")
    return True


# Define the approximate boundaries of the Indian Ocean
min_lat = -40
max_lat = 30
min_lon = 20
max_lon = 100

# Define the time range for the data
start_time = datetime.datetime(2023, 1, 1)
end_time = datetime.datetime(2024, 8, 31)

# Generate waypoints with a 0.5 degree interval, avoiding landmasses and duplicates
with open('indian_ocean_waypoints.csv', 'w', newline='') as csvfile:
    fieldnames = ['latitude', 'longitude', 'elevation', 'timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    used_coordinates = set()  # Store used coordinates to avoid duplicates

    latitude = min_lat
    while latitude <= max_lat:
        longitude = min_lon
        while longitude <= max_lon:
            coordinate_string = f"{latitude},{longitude}"
            if coordinate_string not in used_coordinates:
                # Wrap is_land call with TimeoutFixed
                is_land_thread = TimeoutFixed(
                    is_land, latitude, longitude, timeout=6)
                is_land_thread.join_with_timeout()

                if is_land_thread.result is not None and not is_land_thread.result:
                    elevation = 0  # Assuming sea level
                    timestamp = start_time + \
                        datetime.timedelta(seconds=random.randint(
                            0, (end_time - start_time).total_seconds()))

                    writer.writerow({'latitude': latitude, 'longitude': longitude,
                                     'elevation': elevation, 'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')})
                    used_coordinates.add(coordinate_string)
                else:
                    print(
                        f"Skipped coordinates: {latitude}, {longitude} due to timeout or error.")

            longitude += 1.8
        latitude += 1.8
