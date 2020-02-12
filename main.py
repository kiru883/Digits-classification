from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route("/hook", methods=["POST", "GET"])
def get_image():
    if request.method == "POST":
        test = request.values['test']
        print(test)
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

