import pandas as pd
import math

# Haversine formula to calculate distance between two latitude-longitude points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Fuel consumption model
def calculate_fuel(distance, fuel_per_km=1.0):
    return distance * fuel_per_km

# Pathfinding algorithm (K* logic with fuel consumption constraint)
def find_paths(data, total_fuel, fuel_threshold_ratio=0.8):
    paths = []
    fuel_threshold = total_fuel * fuel_threshold_ratio
    n = len(data)
    
    def dfs(current_path, current_fuel, pos):
        if pos == n - 1:  # Reached the destination
            if current_fuel <= fuel_threshold:
                paths.append((current_path[:], current_fuel))
            return
        
        for next_pos in range(pos + 1, n):
            lat1, lon1 = data[pos]
            lat2, lon2 = data[next_pos]
            distance = haversine(lat1, lon1, lat2, lon2)
            fuel_used = calculate_fuel(distance)
            
            if current_fuel + fuel_used <= fuel_threshold:
                current_path.append(next_pos)
                dfs(current_path, current_fuel + fuel_used, next_pos)
                current_path.pop()
    
    # Start DFS from point 0 (A) to point n-1 (B)
    dfs([0], 0, 0)
    
    return paths

# Read the data from CSV
file_path = 'data/indian_ocean_waypoints.csv'
df = pd.read_csv(file_path)

# Extract latitude and longitude from the file
waypoints = df[['latitude', 'longitude']].values.tolist()

# Get user input for start and end points
start_lat = float(input("Enter the starting latitude: "))
start_lon = float(input("Enter the starting longitude: "))
end_lat = float(input("Enter the ending latitude: "))
end_lon = float(input("Enter the ending longitude: "))

# Insert the user-provided start and end points into the waypoints list
waypoints.insert(0, [start_lat, start_lon])  # Add start point at the beginning
waypoints.append([end_lat, end_lon])         # Add end point at the end

# Example usage
total_fuel = float(input("Enter total fuel available: "))  # Get user input for fuel
paths = find_paths(waypoints, total_fuel)

# Output all valid paths and their fuel consumption
for path, fuel_used in paths:
    # Convert the indices back to latitude and longitude for display
    actual_path = [waypoints[i] for i in path]
    print(f"Path: {actual_path}, Fuel Used: {fuel_used:.2f}")

