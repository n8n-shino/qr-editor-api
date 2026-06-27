from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import json
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "QR Editor API is running!"

@app.route("/move-qr", methods=["POST"])
def move_qr():

    # Read uploaded image
    if "image" not in request.files:
        return "Missing image", 400

    file = request.files["image"]

    img = Image.open(file).convert("RGB")

    # Read coordinates JSON
    if "coordinates" not in request.form:
        return "Missing coordinates", 400

    data = json.loads(request.form["coordinates"])

    qr = data["qr_block"]
    date = data["date_issued"]

    draw = ImageDraw.Draw(img)

    # Crop QR block
    qr_crop = img.crop((
        qr["left"],
        qr["top"],
        qr["right"],
        qr["bottom"]
    ))

    # Remove original QR block
    draw.rectangle(
        (
            qr["left"],
            qr["top"],
            qr["right"],
            qr["bottom"]
        ),
        fill="white"
    )

    # Paste below Date Issued
    margin = 15

    dest_x = date["left"]
    dest_y = date["bottom"] + margin

    img.paste(
        qr_crop,
        (
            dest_x,
            dest_y
        )
    )

    output = io.BytesIO()

    img.save(output, format="PNG")

    output.seek(0)

    return send_file(
        output,
        mimetype="image/png"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
