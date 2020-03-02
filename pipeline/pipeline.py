from PIL import Image, ImageChops
from sklearn.preprocessing import MinMaxScaler
from skimage.transform import resize
from io import BytesIO
from joblib import load
import numpy
import base64
import matplotlib.pyplot as plt
from FNN import FNN
import sklearn
import tensorflow
import lightgbm


global GRAPH
GRAPH = tensorflow.get_default_graph()
MODEL_FILE_EXTENSION = ".joblib"
MODELS_PATH = "pipeline/models"
IMG_SIZES = {
    "input_img": (180, 170),
    "bounded_img": (120, 116),
    "mnist_img": (100, 90)
}

class Model:
    def __init__(self, image_noise_coef):
        # load models is model path with model_file_extension
        self.__dnn_model = load("pipeline/models/DNN.joblib")
        self.__cnn_model = load("pipeline/models/CNN.joblib")
        self.__gb_model = load("pipeline/models/GB.joblib")
        self.__logreg_ensamble_model = load("pipeline/models/LogRegEnsamble.joblib")

        self.mnist_image = None
        self.predicts = None
        self.cnn_pred = None
        self.dnn_pred = None
        self.gb_pred = None
        self.image_noise_coef = image_noise_coef

    # image preprocessor, return 3 image for site and 'mnist-array' image
    def image_preprocessing(self, imgB64):
        # get image from tmp files, (reopen, fix???)
        image = Image.open(BytesIO(base64.b64decode(imgB64)))

        # get bounding rect
        bbox = image.getbbox()

        # get width and height of bounding rect
        widthlen = bbox[2] - bbox[0]
        heightlen = bbox[3] - bbox[1]

        # convert in numpy array
        number = list(image.crop(bbox).getdata())
        number = numpy.array([px[3] for px in number]).reshape(heightlen, widthlen)

        # proportionally resizing(largest side equated is 20)
        if widthlen >= heightlen:
            heightlen = int((heightlen * 20) / widthlen)
            widthlen = 20
        else:
            widthlen = int((widthlen * 20) / heightlen)
            heightlen = 20
        number = resize(number, (heightlen, widthlen))

        # get mnist image
        number = numpy.around(MinMaxScaler().fit_transform(number) * 255).astype(int)
        half_y = heightlen // 2
        half_x = widthlen // 2
        self.mnist_image = numpy.zeros((28, 28))
        self.mnist_image[14 - (half_y):14 + (heightlen - half_y), 14 - (half_x):14 + (widthlen - half_x)] = number
        self.mnist_image = MinMaxScaler().fit_transform(self.mnist_image)

        # prepare images from site put in preprocessed part
        image64 = self.__site_images_prepare(image, "input_img")
        bounded64 = self.__site_images_prepare(image.crop(bbox), "bounded_img")
        mnist64 = self.__site_images_prepare(self.mnist_image, "mnist_img")

        del image, number, half_x, half_y, widthlen, heightlen
        return {
            "input_image": image64,
            "bounded_digit": bounded64,
            "mnist_image": mnist64
        }

    # predicts stage, return predicts for each model
    def predict(self):
        # need for keras model, cnn predict
        with GRAPH.as_default():
            self.cnn_pred = self.__cnn_model.predict_proba(self.mnist_image.reshape(-1, 28, 28, 1))[0]
        # dnn predict
            self.dnn_pred = self.__dnn_model.predict_proba(self.mnist_image.reshape(1, -1))[0][0]
        # gradient boosting predict
            self.gb_pred = self.__gb_model.predict_proba(self.mnist_image.reshape(1, -1))[0]

        # around arrays
        cnn_pred = numpy.around(self.cnn_pred, 3)
        dnn_pred = numpy.around(self.dnn_pred, 3)
        gb_pred = numpy.around(self.gb_pred, 3)

        return {
            'DNN': dnn_pred.tolist(),
            'CNN': cnn_pred.tolist(),
            'GB': gb_pred.tolist()
        }

    # predict number by ensamble using predicts of each models
    def ensamble_predict(self):
        # create matrix with probabilities(each columns is each model predict)
        numbers_probabilities = numpy.concatenate([self.dnn_pred.reshape(1, -1),
                                                  self.cnn_pred.reshape(1, -1),
                                                  self.gb_pred.reshape(1, -1)], axis=1)
        # get predict
        number_probabilities = self.__logreg_ensamble_model.predict_proba(numbers_probabilities).flatten()
        number = numpy.argmax(number_probabilities)
        return {
            'number': int(number),
            'probability': number_probabilities[number]
        }

    # prepare image for site
    def __site_images_prepare(self, image, img_type):
        # convert in image if image is array
        if type(image) == numpy.ndarray:
            buf = BytesIO()
            plt.imshow(image, cmap='Greys', interpolation='nearest')
            plt.axis('off')
            plt.savefig(buf, bbox_inches='tight')
            image = Image.open(buf)

        # get images background and image sizes
        width_b, height_b = IMG_SIZES[img_type]
        width_i, height_i = image.size

        # find max and min background sizes
        max_b, min_b = (width_b, height_b) if width_b > height_b else (height_b, width_b)

        # prop. resizing
        if width_i >= height_i:
            height_i = int((height_i * max_b) / width_i)
            width_i = max_b
        else:
            width_i = int((width_i * max_b) / height_i)
            height_i = max_b
        image = image.resize((width_i, height_i))

        # get site image
        site_image = Image.new(mode='RGBA', size=(width_b, height_b), color=255)
        site_image.paste(image, (width_b//2 - width_i//2, height_b//2 - height_i//2))

        # write image in buffer(base64)
        buffer = BytesIO()
        site_image.save(buffer, format="PNG")

        img = base64.b64encode(buffer.getvalue()).decode('ascii')

        del image, site_image, max_b, min_b, width_i, width_b, height_i, height_b, buffer
        return img








