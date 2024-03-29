from flask import Flask, render_template, request, jsonify
from pipeline.pipeline import Model
import os
import gc


NOISE_COEF = 32
app = Flask(__name__)
model = None
images = None
predicts = None
ensamble = None


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')


@app.route("/hook", methods=["POST", "GET"])
def get_image():
    success_compute = False
    if request.method == "POST":
        # get post req.
        image_base64 = request.values['imageBase64']
        image_base64 = image_base64.split(',')[1].encode('utf-8')

        # part 1, image preprocessing
        images = model.image_preprocessing(image_base64)

        # part 2, predict
        predicts = model.predict()

        # part 3, ansamble
        ensamble = model.ensamble_predict()

        success_compute = True
        del image_base64
        gc.collect()

    return jsonify({
        "images": images,
        "predicts": predicts,
        "ensamble": ensamble,
        "success_compute": success_compute
    })


def load_model():
    global model
    model = Model(image_noise_coef=NOISE_COEF)


if __name__ == '__main__':
    load_model()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

