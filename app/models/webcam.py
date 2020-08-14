from threading import Lock
import cv2.cv2 as cv2
import numpy
import time
from app.models.rectangle import Rectangle


class Webcam():
    def __init__(self):
        self.webcam_port = 0
        self.video_stream = None
        self.output_frame = None
        self.uploaded_image = None
        self.lock_frame = Lock()
        self.lock_uploaded_image = Lock()
        self.rectangle = Rectangle()
        self.trying_get_webcam_image = True
    

    def init_webcam(self):
        with self.lock_frame:
            if self.is_invalid_webcam() or not self.trying_get_webcam_image:
                self.video_stream = cv2.VideoCapture(self.webcam_port) #, cv2.CAP_DSHOW
                self.trying_get_webcam_image = True


    def is_invalid_webcam(self):
        return self.video_stream is None or not self.video_stream.isOpened()
    
    def get_frame_shape(self):
        with self.lock_frame:
            if self.is_invalid_webcam():
                height, width, got_image = (480, 640, False)
            else: 
                sucess, frame = self.video_stream.read()
                height, width, _ = frame.shape if sucess else (480, 640, 0)
                got_image = True if sucess else False
            return {
                "style": f"style=height:{height}px;min-height:{height}px;width:{width}px;min-width:{width}px;",
                "got_image": got_image,
            }


    def __del__(self):
        self.turn_off_webcam()
    

    def turn_off_webcam(self):
        with self.lock_frame:
            if self.video_stream is not None:
                self.video_stream.release()
                self.video_stream = None


    def get_image(self):
        with self.lock_uploaded_image:
            if isinstance(self.uploaded_image, numpy.ndarray):
                return self.get_uploaded_image()
        return self.get_webcam_image()
    

    def get_uploaded_image(self):
        copy = self.uploaded_image.copy()
        return self.convert_to_bytes(self.draw_rectangle_on_image(copy))
        
    
    def get_webcam_image(self):
        with self.lock_frame:
            if not self.is_invalid_webcam():
                frame = self.get_new_frame()
            else:
                frame = self.black_image()
        self.output_frame = frame.copy()
        return self.convert_to_bytes(self.draw_rectangle_on_image(frame))
    

    def get_new_frame(self):
        if self.trying_get_webcam_image:
            sucess, frame = self.video_stream.read()
            if sucess:
                return frame
            else:
                self.trying_get_webcam_image = False
                return self.black_image()
        else:
            return self.black_image()
    

    def black_image(self):
        return numpy.zeros((480, 640, 3), numpy.uint8)
                

    def convert_to_bytes(self, image):
        return self.encode_to_jpg(image).tobytes()
    

    def encode_to_jpg(self, image):
        return cv2.imencode(".jpg", image)[1]


    def draw_rectangle_on_image(self, frame):
        if self.rectangle.is_valid_rectangle():
            cv2.rectangle(img = frame, color = (0, 0, 255), thickness = 1,
                pt1 = self.rectangle.initial_xy(), pt2 = self.rectangle.final_xy())
        return frame


    def clear(self):
        self.turn_off_webcam()
        self.clear_rectangle_and_uploaded_image()
    

    def clear_rectangle_and_uploaded_image(self):
        self.rectangle.initial_points_of_rectangle()
        with self.lock_uploaded_image:
            self.uploaded_image = None
        

    def get_differentiator_image(self):
        with self.lock_uploaded_image and self.rectangle.lock_drawing:
            if isinstance(self.uploaded_image, numpy.ndarray):
                copy = self.uploaded_image.copy()
                self.uploaded_image = None
                return self.rectangle.crop_image(copy)
        return self.selected_rectangle_image()


    def selected_rectangle_image(self):
        with self.lock_frame and self.rectangle.lock_drawing:
            return self.rectangle.crop_image(self.output_frame)


    # def generate(self):
    #     while True:
    #         init_response = b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'
    #         yield(init_response + self.get_image() + b'\r\n\r\n')
    #         time.sleep(0.1)
    

    def generate(self):
        FRAME_RATE = 0.1
        previous = 0
        while True:
            img = self.get_image()
            if (time.time() - previous) > (FRAME_RATE):
                previous = time.time()
                yield(b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

    
    def save_uploaded_image(self, image):
        if image:
            numpy_img = numpy.fromstring(image.read(), numpy.uint8)
            cv2_image = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
            cv2_image = self.resize_image(cv2_image)
            with self.lock_uploaded_image:
                self.uploaded_image = cv2_image
    

    def resize_image(self, image):
        with self.lock_frame:
            size = self.output_frame.shape
            return cv2.resize(image, (size[1], size[0]))


