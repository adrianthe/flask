from flask import Flask, request, jsonify, send_from_directory
import subprocess
import requests
import uuid
import os

app = Flask(__name__)
OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/add_overlay", methods=["POST"])
def add_overlay():
    try:
        data = request.get_json()
        video_url = data.get("videoUrl")
        overlay_text = data.get("overlayText", "Default Overlay")

        if not video_url:
            return jsonify({"error": "Missing videoUrl"}), 400

        input_filename = f"input_{uuid.uuid4()}.mp4"
        output_filename = f"output_{uuid.uuid4()}.mp4"
        input_path = os.path.join(OUTPUT_DIR, input_filename)
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # Download video
        response = requests.get(video_url, stream=True)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to download video. Status code: {response.status_code}"}), 400

        with open(input_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Overlay dengan FFmpeg
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-vf", f"drawtext=text='{overlay_text}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=30",
            "-codec:a", "copy",
            output_path
        ]
        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Debug log
        print("FFmpeg stderr:")
        print(result.stderr.decode())

        # Cek output
        if not os.path.exists(output_path):
            return jsonify({"error": "FFmpeg failed to produce output video."}), 500

        # Hapus input (optional)
        os.remove(input_path)

        # Return URL hasil overlay
        public_url = request.host_url + f"static/{output_filename}"
        return jsonify({
            "status": "success",
            "overlay_url": public_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
