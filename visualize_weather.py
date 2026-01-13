import pandas as pd
import plotly.express as px
import glob
import os

# 1. Find all parquet files in the data folder
files = glob.glob("data/*.parquet")

# 2. Read and combine them into one big DataFrame
df_list = [pd.read_parquet(f) for f in files]
all_data = pd.concat(df_list, ignore_index=True)

# 3. Sort by time so the graph looks correct
all_data = all_data.sort_values(by='timestamp')

print(f"Combined {len(files)} files. Ready to graph!")

# 4. Create a Line Chart
fig = px.line(
    all_data, 
    x='timestamp', 
    y='temp_celsius', 
    color='city',
    title='Temperature Trends Across Cities',
    labels={'temp_celsius': 'Temperature (°C)', 'timestamp': 'Time of Reading'}
)

# 5. Show it in your browser
fig.show()

# 6. Print a Daily Summary
print("\n--- Daily Weather Summary ---")
summary = all_data.groupby('city')['temp_celsius'].agg(['min', 'max', 'mean']).round(2)
print(summary)