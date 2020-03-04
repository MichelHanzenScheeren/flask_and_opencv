from threading import Lock, Thread
from imutils import resize
import cv2.cv2 as cv2

class Webcam():
    def __init__(self):
        self.output_frame = None
        self.lock_frame = Lock()
        self.video_stream = cv2.VideoCapture(0) # openCV-python version


    def __del__(self):
        self.video_stream.release()


    def get_image(self, rectangle):
        success, frame = self.video_stream.read() # openCV-python version
        #frame = cv2.flip(frame, 1)  # espelha a imagem
        #frame = resize(frame, 500)  # redimensiona
        with self.lock_frame:
            self.output_frame = frame.copy()
        success, jpeg = cv2.imencode('.jpg', rectangle.draw_rectangle(frame))
        return jpeg.tobytes()

    def generate(self, rectangle):
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.get_image(rectangle) + b'\r\n\r\n')
