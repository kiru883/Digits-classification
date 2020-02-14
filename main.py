from flask import Flask, render_template, request
import base64
from pipeline import pipeline

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route("/hook", methods=["POST", "GET"])
def get_image():
    if request.method == "POST":
        image_base64 = request.values['imageBase64']
        image = base64.decodebytes(image_base64.split(',')[1].encode('utf-8'))
        with open('tmp/input.jpg') as f:
            f.write(image)
        #pipeline image preprocessing#

    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

