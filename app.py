from flask import Flask, render_template, send_from_directory
from graph_generator import generate_graphs
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Generate new graphs from the latest DB
    generate_graphs()
    graph_files = os.listdir('static/graphs')
    return render_template('homepage.html', graphs=graph_files)

@app.route('/graphs/<filename>')
def get_graph(filename):
    return send_from_directory('static/graphs', filename)

if __name__ == "__main__":
    # Retrieve the PORT environment variable, or default to 5000 if not set
    port = int(os.environ.get("PORT", 5000))
    # Bind the app to 0.0.0.0 on the dynamic port
    app.run(host="0.0.0.0", port=port)
