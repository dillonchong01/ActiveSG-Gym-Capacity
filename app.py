from flask import Flask, render_template, send_from_directory
from graph_generator import generate_graphs
import os
from flask_caching import Cache

app = Flask(__name__)

# Configure the caching system
app.config['CACHE_TYPE'] = 'simple'  # Use in-memory caching for simplicity
app.config['CACHE_DEFAULT_TIMEOUT'] = 86400  # Cache timeout: 1 day (86400 seconds)
cache = Cache(app)

@app.route('/')
# @cache.cached(timeout=86400, key_prefix='graphs')  # Cache the homepage route for 1 day

def home():
    # Generate new graphs from the latest DB
    generate_graphs()
    graph_files = [file for file in os.listdir('public/graphs') if file != '.gitkeep']
    return render_template('homepage.html', graphs=graph_files)

@app.route('/graphs/<filename>')
def get_graph(filename):
    return send_from_directory('public/graphs', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
