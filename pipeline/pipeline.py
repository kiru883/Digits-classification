from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from skimage.transform import resize
import numpy
from io import BytesIO
import base64



class Model:
    def __init__(self, image_noise_coef):
        self.mnist_image = None;
        self.predicts = None;
        self.image_noise_coef = image_noise_coef;

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

        # prepare images from site put in preprocessed part
        self.__site_images_prepare(image, "input_image")
        self.__site_images_prepare(image.crop(bbox), "bounded_digit")
        self.__site_images_prepare(self.mnist_image, "preprocessed_image")

    # prepare image for site
    def __site_images_prepare(self, image, img_type):
        # convert in image if image is array
        if type(image) == numpy.ndarray:
            image = Image.fromarray(image)

        # get images background and image sizes
        width_b, height_b = Image.open("static/images/" + img_type + ".png").size
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

        # save img in tmp folder
        site_image.save("tmp/" + img_type + "_prepared.png")

        del image, site_image, max_b, min_b, width_i, width_b, height_i, height_b








