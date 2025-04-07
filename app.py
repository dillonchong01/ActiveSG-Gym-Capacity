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
    # List all graph filenames
    graph_files = [
        file for file in os.listdir('static/graphs')
        if file.endswith('.png') or file.endswith('.jpg')
    ]

    # Extract unique gym names (remove _weekday or _weekend suffix)
    gym_names = set()
    for file in graph_files:
        name = os.path.splitext(file)[0]
        if name.endswith('_weekday'):
            name = name.removesuffix('_weekday')
        elif name.endswith('_weekend'):
            name = name.removesuffix('_weekend')
        gym_names.add(name)

    return render_template('homepage.html', gyms=sorted(gym_names))

@app.route('/gym/<gym_name>')
def show_gym(gym_name):
    def graph_exists(name):
        for ext in ['.jpg', '.png']:
            path = f"static/graphs/{name}{ext}"
            if os.path.exists(path):
                return f"{name}{ext}"
        return None

    weekday_image = graph_exists(f"{gym_name}_weekday")
    weekend_image = graph_exists(f"{gym_name}_weekend")

    if not weekday_image and not weekend_image:
        return "Gym graphs not found", 404

    return render_template(
        'gym_page.html',
        gym_name=gym_name,
        weekday_image=weekday_image,
        weekend_image=weekend_image
    )

@app.route('/select-gym', methods=['POST'])
def select_gym():
    selected_gym = request.form.get('gym')
    return redirect(url_for('show_gym', gym_name=selected_gym))

if __name__ == "__main__":
    app.run(host="0.0.0.0")