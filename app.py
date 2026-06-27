from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import requests
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "QR Editor API is running!"

@app.route("/move-qr", methods=["POST"])
def move_qr():

    data = request.get_json()

    image_url = data["image_url"]

    qr = data["qr_block"]

    date = data["date_issued"]

    # Download image from Cloudinary
    response = requests.get(image_url)

    response.raise_for_status()

    img = Image.open(io.BytesIO(response.content)).convert("RGB")

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

    # Position below Date Issued
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
