from threading import Lock, Thread
from imutils.video import VideoStream
from imutils import resize
import cv2.cv2 as cv2

class Webcam():
    def __init__(self):
        self.output_frame = None
        self.lock_frame = Lock()
        #self.video_stream = VideoStream(src=0)
        self.video_stream = cv2.VideoCapture(0)
        self.thread = Thread(target=self.get_image, daemon=True)


    def start(self):
        #self.video_stream.start()
        self.thread.start()


    def stop_stream(self):
        self.video_stream.release()


    def get_image(self):
        while True:
            frame = self.video_stream.read()[1]  # obtêm frame da Webcam
            frame = cv2.flip(frame, 1)  # espelha a imagem
            frame = resize(frame, width=600)  # redimensiona
            with self.lock_frame:
                self.output_frame = frame.copy()

    def generate_jpg(self, rectangle):
        while True:
            with self.lock_frame:
                if self.output_frame is None:
                    continue
                (flag, encodedImage) = cv2.imencode(".jpg", rectangle.draw_rectangle(self.output_frame.copy()))  # encode the frame in JPEG format
                if not flag:  # ensure the frame was successfully encoded
                    continue
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')