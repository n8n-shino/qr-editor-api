from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "QR Editor API is running!"

@app.route("/test")
def test():
    return "TEST OK"

@app.route("/move-qr", methods=["POST"])
def move_qr():

    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]

    img = Image.open(file).convert("RGB")

    # Existing QR area
    crop_box = (
        1135,
        595,
        1291,
        830
    )

    qr = img.crop(crop_box)

    draw = ImageDraw.Draw(img)

    # Remove old QR
    draw.rectangle(crop_box, fill="white")

    # Paste below Date Issued
    img.paste(qr, (900, 180))

    output = io.BytesIO()

    img.save(output, format="PNG")

    output.seek(0)

    return send_file(
        output,
        mimetype="image/png"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
