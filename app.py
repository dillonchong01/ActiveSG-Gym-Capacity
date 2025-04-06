import logging
import os
from flask import Flask, render_template, send_from_directory
from graph_generator import *

# Initialize the Flask app and set up logging
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Serve static files from the '/tmp' directory
@app.route('/graphs/<filename>')
def get_graph(filename):
    return send_from_directory('/tmp', filename)

@app.route('/')
def home():
    try:
        logger.debug("Starting graph generation...")
        # Generate new graphs from the latest DB
        generate_all()  # Calling the graph generation function
        graph_files = [file for file in os.listdir('/tmp') if file.endswith('.png')]
        
        logger.debug(f"Graph files found: {graph_files}")
        return render_template('homepage.html', graphs=graph_files)
    except Exception as e:
        logger.error(f"Error generating graphs: {e}")
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0")
