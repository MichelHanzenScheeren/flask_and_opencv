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
    

    def init_webcam(self):
        with self.lock_frame:
            if self.video_stream is None:
                self.video_stream = cv2.VideoCapture(self.webcam_port)


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
        _, jpeg = cv2.imencode(".jpg", self.draw_rectangle_on_image(copy))
        return jpeg.tobytes()
        
    
    def get_webcam_image(self):
        _, frame = self.video_stream.read() if self.video_stream is not None else (None, None)
        with self.lock_frame:
            if frame is None:
                frame = self.output_frame.copy()
            else:
                self.output_frame = frame.copy()
        _, jpeg = cv2.imencode('.jpg', self.draw_rectangle_on_image(frame))
        return jpeg.tobytes()
    

    def draw_rectangle_on_image(self, frame):
        if self.rectangle.is_valid_rectangle():
            cv2.rectangle(img = frame, color = (0, 0, 255), thickness = 1,
                pt1 = self.rectangle.initial_xy(), pt2 = self.rectangle.final_xy())
        return frame


    def define_points_of_rectangle(self, x1, y1, x2, y2):
        self.rectangle.define_points_of_rectangle(x1, y1, x2, y2)
        
    
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


    def generate(self):
        while True:
            init_response = b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'
            yield(init_response + self.get_image() + b'\r\n\r\n')
            time.sleep(0.1)
    

    # def generate(self):
    #     FRAME_RATE = 0.1
    #     previous = 0
    #     while True:
    #         image = self.get_image()
    #         time_elapsed = time.time()
    #         if (time_elapsed - previous) > (FRAME_RATE):
    #             previous = time_elapsed
    #             init_response = b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'
    #             yield(init_response + image + b'\r\n\r\n')

    
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


