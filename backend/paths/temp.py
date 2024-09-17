import pandas as pd

# Read the data from a CSV file
# Assuming the file is named 'data.csv'
df = pd.read_csv('data//indian_ocean_waypoints.csv')

# Generating 'coordinates' column with continuous unique values
df['coordinates'] = ['c' + str(i+1) for i in range(len(df))]

# Save the updated dataframe back to the CSV file or a new file
df.to_csv('data//updated.csv', index=False)

# Displaying the updated DataFrame
print(df)
