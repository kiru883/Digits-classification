from flask import Flask, render_template, request, url_for
from pipeline.pipeline import Model


app = Flask(__name__)
model = Model(image_noise_coef=15)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html', test='input_image.png')


@app.route("/hook", methods=["POST", "GET"])
def get_image():
    if request.method == "POST":
        # get post req.
        image_base64 = request.values['imageBase64']
        image_base64 = image_base64.split(',')[1].encode('utf-8')

        # part 1, image preprocessing
        model.image_preprocessing(image_base64)
        # rendering, update preprocessing images
        render_template('index.html', test='static(input_image_prepared.png)')



    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

