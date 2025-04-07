import os
import re
import sqlite3
import polars as pl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, datetime
from concurrent.futures import ThreadPoolExecutor


def generate_all():
    os.makedirs("static/graphs", exist_ok=True)
    # Connect to the SQLite database
    conn = sqlite3.connect("database/gym_capacity_summary.db")

    # Load raw data from the database
    query = "SELECT gym_name, time, capacity, is_weekend FROM gym_capacity_summary;"
    df = pl.read_database(query, conn)
    conn.close()

    # Group by gym_name and time and obtain average capacity
    df = df.with_columns(pl.col("time").str.strptime(pl.Time, "%H:%M").alias("time"))
    
    df_grouped = (df.group_by(["gym_name", "time", "is_weekend"])
                  .agg(pl.col("capacity").mean().alias("capacity"))
                  .sort(["gym_name", "is_weekend", "time"])
                 )

    # Use ThreadPoolExecutor to generate graphs concurrently for each gym
    with ThreadPoolExecutor() as executor:
        # Submit graph generation tasks for each gym and weekend pair in parallel
        futures = [
            executor.submit(generate_graph, gym, bool(weekend),
                df_grouped.filter((pl.col("gym_name") == gym) & (pl.col("is_weekend") == weekend)))
            for gym in df_grouped["gym_name"].unique()
            for weekend in [0, 1]
        ]
                
        # Wait for all futures to complete
        for future in futures:
            future.result()

def generate_graph(gym, is_weekend, gym_data):
    gym = re.sub(r'\s+', ' ', gym)
    # Sort by time, obtain list of times and capacities
    gym_data = gym_data.sort("time")
    times = [datetime.combine(date.today(), t) for t in gym_data["time"]]
    capacities = gym_data["capacity"].to_list()

    if not times or not capacities:
        return

    # Plot graph
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
    ax.plot(times, capacities, marker="o", linestyle="-", linewidth=2, markersize=5, color="blue")
    label = "Weekend" if is_weekend else "Weekday"
    ax.set_title(f"Gym Capacity - {gym} ({label})")
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("Average Capacity")

    # Set x and y axis
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylim(0, min(100, max(capacities) + 10))

    ax.grid(True)
    fig.tight_layout()

    # Save graph into static/graphs
    filename = re.sub(r'[^\w\-_. @]', '_', gym)
    filename = re.sub(r'\s+', '_', filename) + f'_{label.lower()}'
    graph_path = f"static/graphs/{filename}.jpg"
    fig.savefig(graph_path, facecolor='white', edgecolor='white')
    plt.close(fig)

if __name__ == "__main__":
    generate_all()