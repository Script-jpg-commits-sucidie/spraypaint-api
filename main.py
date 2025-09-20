from flask import Flask, request, jsonify
from PIL import Image
import io
import requests
import os

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_image():
    data = request.json
    url = data.get("url")
    max_size = data.get("max_size", 200)

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        resp = requests.get(url)
        img = Image.open(io.BytesIO(resp.content)).convert("RGBA")

        if max_size:
            img.thumbnail((max_size, max_size), Image.LANCZOS)

        width, height = img.size
        pixels = []

        for y in range(height):
            row = []
            for x in range(width):
                r, g, b, a = img.getpixel((x, y))
                row.append([r, g, b, a])
            pixels.append(row)

        return jsonify({"width": width, "height": height, "pixels": pixels})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
