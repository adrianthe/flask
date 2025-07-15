from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask on Railway!"

@app.route("/edit", methods=["POST"])
def edit():
    data = request.get_json()
    video_url = data.get("videoUrl")
    return jsonify({"status": "success", "received_url": video_url})
