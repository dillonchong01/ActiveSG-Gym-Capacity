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
    # Check if we are on Render (cloud environment)
    if os.environ.get("RENDER"):
        print("App is running in a cloud environment. Starting app...")
        # Run the app on all network interfaces and on the dynamically assigned port
        port = int(os.environ.get("PORT", 10000))  # Render sets the PORT environment variable
        app.run(host="0.0.0.0", port=port)
    else:
        print("App is not running in a cloud environment. Exiting.")
        # Prevent running the Flask app locally
        # You can log, exit, or print a message indicating that the app is not running locally.
        exit(0)
