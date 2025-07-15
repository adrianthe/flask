from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Railway!'

@app.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    video_url = data.get('videoUrl')
    return jsonify({"message": f"Video URL received: {video_url}"})
