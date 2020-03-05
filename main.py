from flask import Flask, render_template, request, jsonify
from pipeline.pipeline import Model
import os


app = Flask(__name__)
model = Model(image_noise_coef=15)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')


@app.route("/hook", methods=["POST", "GET"])
def get_image():
    if request.method == "POST":
        # get post req.
        global images
        global predicts
        global ensamble
        image_base64 = request.values['imageBase64']
        image_base64 = image_base64.split(',')[1].encode('utf-8')

        # part 1, image preprocessing
        images = model.image_preprocessing(image_base64)
        # part 2, predict
        predicts = model.predict()

        # part 3, ansamble
        ensamble = model.ensamble_predict()

    return jsonify({
        "images": images,
        "predicts": predicts,
        "ensamble": ensamble
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

