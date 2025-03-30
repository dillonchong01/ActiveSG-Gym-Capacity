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
