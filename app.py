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

    file = request.files["image"]

    img = Image.open(file).convert("RGB")

    draw = ImageDraw.Draw(img)

    left = int(request.form["left"])
    top = int(request.form["top"])
    right = int(request.form["right"])
    bottom = int(request.form["bottom"])

    date_left = int(request.form["date_left"])
    date_bottom = int(request.form["date_bottom"])

    qr = img.crop((left, top, right, bottom))

    draw.rectangle(
        (left, top, right, bottom),
        fill="white"
    )

    margin = 15

    img.paste(
        qr,
        (
            date_left,
            date_bottom + margin
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
