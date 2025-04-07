import re
import sqlite3
import polars as pl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor


def generate_all():
    # Connect to the SQLite database
    conn = sqlite3.connect("database/gym_capacity_summary.db")

    # Load raw data from the database
    query = "SELECT gym_name, time, capacity FROM gym_capacity_summary;"
    df = pl.read_sql(query, conn)
    conn.close()

    # Group by gym_name and time and obtain average capacity
    df = df.with_columns(pl.col("time").dt.time())
    df_grouped = (df.groupby(["gym_name", "time"])
                  .agg(pl.col("capacity").mean().alias("capacity"))
                  .sort(["gym_name", "time"])
                 )

    # Use ThreadPoolExecutor to generate graphs concurrently for each gym
    with ThreadPoolExecutor() as executor:
        # Submit graph generation tasks for each gym in parallel
        futures = [executor.submit(generate_graph, gym, df_grouped.filter(pl.col("gym_name") == gym))
                   for gym in df_grouped["gym_name"].unique()]
                
        # Wait for all futures to complete
        for future in futures:
            future.result()

def generate_graph(gym, gym_data):
    # Define x-axis labels
    desired_ticks = [datetime.strptime(f"{hour:02d}:00", "%H:%M") for hour in range(7, 23)]
    desired_tick_labels = [dt.strftime("%H:%M") for dt in desired_ticks]

    # Obtain data for plotting
    times = [datetime.strptime(str(t), "%H:%M").time() for t in gym_data["time"].to_list()]
    capacities = gym_data["capacity"].to_list()
        
    # Generate and save the graph for each gym
    plt.figure(figsize=(8, 5))
    plt.plot(times,capacities, marker="o", linestyle="-")
    plt.xlabel("Time of Day")
    plt.ylabel("Average Capacity")
    plt.title(f"Gym Capacity - {gym}")
    plt.xticks(ticks=desired_ticks, labels=desired_tick_labels, rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save graph as an image in 'static/graphs'
    filename = re.sub(r'[^\w\-_. ]', '_', gym).replace(' ', '_')
    graph_path = f"static/graphs/{filename}.png"
    plt.savefig(graph_path)
    plt.close()

if __name__ == "__main__":
    generate_all()
