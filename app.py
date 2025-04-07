import os
from flask import Flask, render_template, send_from_directory, redirect, url_for, request

# Initialize the Flask app and set up logging
app = Flask(__name__)

# Serve static files from the '/tmp' directory
@app.route('/graphs/<filename>')
def get_graph(filename):
    return send_from_directory('static/graphs', filename)

@app.route('/')
def home():
    graph_files = [file for file in os.listdir('static/graphs')
                   if file.endswith('.png') or file.endswith('.jpg')]
    # Strip file extensions to get gym names
    gym_names = [os.path.splitext(f)[0] for f in graph_files]
        
    return render_template('homepage.html', gyms=sorted(gym_names))

@app.route('/gym/<gym_name>')
def show_gym(gym_name):
    # Match corresponding image file
    for ext in ['.png', '.jpg']:
        path = f"static/graphs/{gym_name}{ext}"
        if os.path.exists(path):
            return render_template('gym_page.html', gym_name=gym_name, image_file=f"{gym_name}{ext}")
    return "Gym graph not found", 404

@app.route('/select-gym', methods=['POST'])
def select_gym():
    selected_gym = request.form.get('gym')
    return redirect(url_for('show_gym', gym_name=selected_gym))

if __name__ == "__main__":
    app.run(host="0.0.0.0")