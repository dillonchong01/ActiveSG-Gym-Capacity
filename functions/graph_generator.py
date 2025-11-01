import os
import re
import sqlite3
import polars as pl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns
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
    # --- Dark modern theme setup ---
    plt.style.use('dark_background')
    sns.set_style("whitegrid", {'axes.facecolor': '#1b1528'})
    gym = re.sub(r'\s+', ' ', gym)

    # Sort and prepare data
    gym_data = gym_data.sort("time")
    times = [datetime.combine(date.today(), t) for t in gym_data["time"]]
    capacities = gym_data["capacity"].to_list()
    if not times or not capacities:
        return

    # --- Create figure ---
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#1b1528')
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # Line color gradient based on theme
    line_color = "#ff7eb3" if is_weekend else "#7dd3fc"  # pink for weekend, blue for weekday
    marker_color = "#ffd1dc" if is_weekend else "#bae6fd"

    ax.plot(
        times, capacities,
        marker="o",
        markersize=6,
        linewidth=2.5,
        color=line_color,
        markerfacecolor=marker_color,
        markeredgecolor='white',
        alpha=0.95
    )

    # --- Title & labels ---
    label = "Weekend" if is_weekend else "Weekday"
    ax.set_title(
        f"{gym} ({label})",
        fontsize=16,
        fontweight='bold',
        color="#f9a8d4" if is_weekend else "#93c5fd",
        pad=15
    )
    ax.set_xlabel("Time", fontsize=13, color="#e5e7eb", labelpad=10)
    ax.set_ylabel("Average Capacity (%)", fontsize=13, color="#e5e7eb", labelpad=10)

    # --- X-axis formatting ---
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    def time_fmt(x, pos=None):
        dt = mdates.num2date(x)
        return dt.strftime('%I%p').lstrip('0')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(time_fmt))

    # --- Y-axis settings ---
    ax.set_ylim(0, min(100, max(capacities) + 10))
    ax.tick_params(axis='x', colors='#d1d5db', labelsize=10)
    ax.tick_params(axis='y', colors='#d1d5db', labelsize=10)

    # --- Grid and frame ---
    ax.grid(color='#2e2a3b', linestyle='-', linewidth=0.7, alpha=0.6)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # --- Glow effect (soft outer line) ---
    for n in range(1, 4):
        ax.plot(times, capacities,
                linewidth=2 + n*1.2,
                color=line_color,
                alpha=0.08 * (4 - n))

    # --- Subtle gradient background ---
    fig.patch.set_facecolor("#1b1528")
    ax.set_facecolor("#241b33")

    # --- Adjust layout and save ---
    fig.subplots_adjust(left=0.12, right=0.95, top=0.9, bottom=0.18)
    filename = re.sub(r'[^\w\-_. @]', '_', gym)
    filename = re.sub(r'\s+', '_', filename) + f'_{label.lower()}'
    graph_path = f"static/graphs/{filename}.jpg"

    fig.savefig(graph_path, facecolor=fig.get_facecolor(), dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated: {graph_path}")

if __name__ == "__main__":
    generate_all()