from flask import Flask, render_template, request, url_for, jsonify, Response
from pipeline.pipeline import Model
import json

import time


app = Flask(__name__)
model = Model(image_noise_coef=15)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')


@app.route("/hook", methods=["POST", "GET"])
def get_image():

    if request.method == "POST":
        # get post req.
        global visualisation_images
        image_base64 = request.values['imageBase64']
        image_base64 = image_base64.split(',')[1].encode('utf-8')

        # part 1, image preprocessing
        visualisation_images = model.image_preprocessing(image_base64)

        # part 2, predict
        print(model.predict())

    return jsonify({
      "images": visualisation_images
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

