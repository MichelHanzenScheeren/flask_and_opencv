import cv2.cv2 as cv2
import numpy


class MyOpencv():

    @staticmethod
    def new_stream(port):
        return cv2.VideoCapture(port)
    

    @staticmethod
    def webcans_list(current_port):
        list_webcans = []
        index = 0
        while True:
            if index == current_port:
                list_webcans.append(index)
            else:
                video = MyOpencv.new_stream(index)
                if video is None or not video.isOpened():
                    break
                list_webcans.append(index)
            index += 1
        return list_webcans


    @staticmethod
    def draw_rectangle(frame, initial_xy, final_xy):
        red_color = (0, 0, 255) # formato bgr (no lugar de rgb)
        cv2.rectangle(frame, initial_xy, final_xy, red_color, thickness = 1)


    @staticmethod
    def convert_to_bytes(image):
        return MyOpencv.encode_to_jpg(image).tobytes()


    @staticmethod
    def encode_to_jpg(image):
        return cv2.imencode(".jpg", image)[1]
    

    @staticmethod
    def convert_to_frame(image):
        numpy_img = numpy.fromstring(image.read(), numpy.uint8)
        cv2_image = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
        return cv2_image
    

    @staticmethod
    def resize_image(image, dimensions):
        h, w = dimensions
        return cv2.resize(image, (w, h))
    

    @staticmethod
    def black_image():
        return numpy.zeros((480, 640, 3), numpy.uint8)
    

    @staticmethod
    def validate_image(image):
        return isinstance(image, numpy.ndarray)
