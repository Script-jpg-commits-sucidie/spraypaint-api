from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ SprayPaint API is running on Railway!"

@app.route("/convert", methods=["GET"])
def convert():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No image url provided"}), 400

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img = img.resize((64, 64))  # smaller = faster

        points = []
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = img.getpixel((x, y))
                if (r, g, b) != (255, 255, 255):  # skip white pixels
                    points.append({
                        "x": x,
                        "y": y,
                        "color": [r/255, g/255, b/255]
                    })

        return jsonify({"points": points})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
