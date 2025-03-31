from flask import Flask, render_template, send_from_directory
from graph_generator import generate_graphs
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Generate new graphs from the latest DB
    generate_graphs()
    graph_files = [file for file in os.listdir('static/graphs') if file != '.gitkeep']
    return render_template('homepage.html', graphs=graph_files)

@app.route('/graphs/<filename>')
def get_graph(filename):
    return send_from_directory('static/graphs', filename)

if __name__ == "__main__":
    # Get the PORT environment variable for Render (or fallback to 10000 locally)
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 for local testing
    # Run the app on all network interfaces with the dynamic port
    app.run(host="0.0.0.0", port=port)
