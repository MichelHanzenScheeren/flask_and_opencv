from threading import Lock
import cv2.cv2 as cv2
from time import sleep
from app.models.rectangle import Rectangle


class Webcam():
    def __init__(self):
        self.output_frame = None
        self.lock_frame = Lock()
        self.video_stream = cv2.VideoCapture(0)
        self.rectangle = Rectangle()


    def __del__(self):
        self.video_stream.release()


    def get_image(self):
        _, frame = self.video_stream.read()
        with self.lock_frame:
            self.output_frame = frame.copy()
        _, jpeg = cv2.imencode('.jpg', self.draw_rectangle_on_image(frame))
        return jpeg.tobytes()


    def draw_rectangle_on_image(self, frame):
        if (self.rectangle.is_valid_rectangle()):
            cv2.rectangle(img = frame, color = (0, 0, 255), thickness = 1,
                pt1 = self.rectangle.initial_xy(), pt2 = self.rectangle.final_xy())
        return frame


    def define_points_of_rectangle(self, x1, y1, x2, y2):
        self.rectangle.define_points_of_rectangle(x1, y1, x2, y2)
    

    def clear_points_of_rectangle(self):
        self.rectangle.clear_points_of_rectangle()
        

    def selected_rectangle_image(self):
        with self.lock_frame and self.rectangle.lock_drawing:
            return self.output_frame[self.rectangle.y_initial:self.rectangle.y_final,self.rectangle.x_initial:self.rectangle.x_final]


    def generate(self):
        while True:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + self.get_image() + b'\r\n\r\n')
            sleep(0.1)

