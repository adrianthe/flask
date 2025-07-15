from flask import Flask, request, jsonify
import subprocess
import requests
import uuid
import os

app = Flask(__name__)

@app.route("/edit", methods=["POST"])
def edit_video():
    data = request.get_json()
    video_url = data.get("videoUrl")
    if not video_url:
        return jsonify({"error": "Missing videoUrl"}), 400

    uid = str(uuid.uuid4())
    filename = f"/tmp/{uid}_input.mp4"
    output = f"/tmp/{uid}_output.mp4"
    overlay = "overlay.png"  # ganti nama file jika perlu

    # Download video
    with open(filename, "wb") as f:
        f.write(requests.get(video_url).content)

    # Jalankan FFmpeg
    cmd = [
        "ffmpeg", "-i", filename, "-i", overlay,
        "-filter_complex", "[0:v][1:v]overlay=10:10,drawtext=text='HOOK GOKIL!':x=20:y=20:fontsize=48:fontcolor=white",
        "-c:a", "copy", output
    ]
    subprocess.run(cmd, check=True)

    # Simpan output ke folder public
    os.makedirs("static", exist_ok=True)
    final_path = f"static/{uid}.mp4"
    os.rename(output, final_path)

    return jsonify({
        "status": "done",
        "editedVideoUrl": request.host_url + final_path
    })

# Gunakan PORT dari Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
