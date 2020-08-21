from threading import Lock
import cv2.cv2 as cv2
import numpy
import time
from app.models.rectangle import Rectangle


class Webcam():
    def __init__(self):
        self.webcam_port = 0
        self.rectangle = Rectangle()

        self.video_stream = None
        self.lock_video_stream = Lock()

        self.success_frame = True
        self.output_frame = None
        self.lock_frame = Lock()

        self.uploaded_image = None
        self.lock_uploaded_image = Lock()
    

    def init_webcam(self):
        if not self.is_valid_webcam() or not self.is_getting_frames():
            self.set_success_frame(True)
            self.start_video_stream()
            self.define_resolution()
    

    def is_valid_webcam(self):
        with self.lock_video_stream:
            return self.video_stream and self.video_stream.isOpened()
    

    def is_getting_frames(self):
        with self.lock_frame:
            return self.success_frame


    def set_success_frame(self, condition = True):
        with self.lock_frame:
            self.success_frame = condition
    

    def start_video_stream(self):
        with self.lock_video_stream:
            self.video_stream = cv2.VideoCapture(self.webcam_port) #, cv2.CAP_DSHOW


    def define_resolution(self):
        with self.lock_video_stream:
            if(self.video_stream.get(3) != 640 or self.video_stream.get(4) != 480):
                self.video_stream.set(3, 640)
                self.video_stream.set(4, 480)
    

    def get_frame_shape(self):
        if not self.is_valid_webcam():
            h, w, success = (480, 640, False)
            self.set_success_frame(False)
        else:
            h, w, _ = self.new_frame().shape
            success = self.is_getting_frames()
        return {"style": f"style=height:{h}px;min-height:{h}px;width:{w}px;min-width:{w}px;","success": success}


    def new_frame(self):
        with self.lock_video_stream:
            success, frame = self.video_stream.read()
        self.set_success_frame(success)
        return frame if success else self.black_image()
    

    def black_image(self):
        return numpy.zeros((480, 640, 3), numpy.uint8)
    

    def generate(self):
        FRAME_RATE, previous = 0.1, 0
        while True:
            img = self.get_image()
            if (time.time() - previous) > (FRAME_RATE):
                previous = time.time()
                yield(b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
    

    def get_image(self):
        if(self.has_uploaded_image()):
            return self.get_uploaded_image()
        return self.get_webcam_image()
    

    def has_uploaded_image(self):
        with self.lock_uploaded_image:
            return isinstance(self.uploaded_image, numpy.ndarray)
    

    def get_uploaded_image(self):
        with self.lock_uploaded_image:
            copy = self.uploaded_image.copy()
        return self.convert_to_bytes(self.draw_rectangle_on_image(copy))
    

    def get_webcam_image(self):
        frame = self.new_frame() if self.can_get_frame() else self.black_image()
        self.set_output_frame(frame.copy())
        return self.convert_to_bytes(self.draw_rectangle_on_image(frame))
    

    def can_get_frame(self):
        return self.is_getting_frames() and self.is_valid_webcam()
    

    def set_output_frame(self, frame):
        with self.lock_frame:
            self.output_frame = frame
    

    def draw_rectangle_on_image(self, frame):
        if self.rectangle.is_valid_rectangle():
            cv2.rectangle(img = frame, color = (0, 0, 255), thickness = 1,
                pt1 = self.rectangle.initial_xy(), pt2 = self.rectangle.final_xy())
        return frame
    

    def convert_to_bytes(self, image):
        return self.encode_to_jpg(image).tobytes()


    def encode_to_jpg(self, image):
        return cv2.imencode(".jpg", image)[1]


    def get_differentiator_image(self):
        if(self.has_uploaded_image()):
            return self.crop_uploaded_image()
        return self.selected_rectangle_image()
    

    def crop_uploaded_image(self):
        with self.lock_uploaded_image:
            copy = self.uploaded_image
            self.uploaded_image = None
        return self.rectangle.crop_image(copy)


    def selected_rectangle_image(self):
        return self.rectangle.crop_image(self.get_output_frame())
    

    def get_output_frame(self):
        with self.lock_frame:
            return self.output_frame


    def save_uploaded_image(self, image):
        if image:
            self.set_uploaded_image(self.convert_image(image))
    

    def convert_image(self, image):
        numpy_img = numpy.fromstring(image.read(), numpy.uint8)
        cv2_image = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
        return self.resize_image(cv2_image)
    

    def resize_image(self, image):
        with self.lock_frame:
            h, w, _ = self.output_frame.shape
        return cv2.resize(image, (w, h))
    

    def set_uploaded_image(self, image):
        with self.lock_uploaded_image:
                self.uploaded_image = image
    

    def clear(self):
        self.turn_off_webcam()
        self.clear_rectangle_and_uploaded_image()
    

    def turn_off_webcam(self):
        with self.lock_video_stream:
            if self.video_stream:
                self.video_stream.release()
                self.video_stream = None
    

    def clear_rectangle_and_uploaded_image(self):
        self.rectangle.initial_points_of_rectangle()
        self.set_uploaded_image(None)
    

    def __del__(self):
        self.turn_off_webcam()

