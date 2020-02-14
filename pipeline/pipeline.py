from PIL import Image



class Model:
    def __init__(self):
        self.mnist_image = None;
        self.predicts = None;

    def image_preprocessing(self):
        # get image from tmp files, (reopen, fix???)
        image = Image.open('input.jpg')

        #  get bounding rect
        bbox = Image.eval(image.convert('1'), lambda px: 255 - px).getbbox()##?

        # get width and height of bounding rect
        widthlen = bbox[2] - bbox[0]
        heightlen = bbox[3] - bbox[1]

        # proportionally resizing(largest side equated is 20)
        if widthlen >= heightlen:
            heightlen = (heightlen * 20) / widthlen
            widthlen = 20
        else:
            widthlen = (widthlen * 20) / heightlen
            heightlen = 20
        number = list(image.crop(bbox).getdata())





        return {'input_image': image,
                'bounding_image': bounding_image,
                'preprocessed_image': preprocessed_image}


    def __get_bounding_rect(self, image):



