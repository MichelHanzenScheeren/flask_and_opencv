from threading import Lock
import time
from app.models.rectangle import Rectangle
from app.models.video_capture import VideoCapture
from app.models.my_opencv import MyOpencv


class Webcam():
    def __init__(self):
        self.current_port = 0
        self.rectangle = Rectangle()
        self.video_capture = VideoCapture()

        self.output_frame = None
        self.lock_frame = Lock()
        self.uploaded_image = None
        self.lock_uploaded_image = Lock()
    

    def init_webcam(self):
        self.video_capture.start_video(self.current_port)
    

    def video_status(self):
        h, w, success = self.video_capture.video_status()
        return {"style": f"height:{h}px;min-height:{h}px;width:{w}px;min-width:{w}px;",
            "success": success, "current": self.current_port}
    

    def webcans_list(self):
        return MyOpencv.webcans_list(self.current_port)


    def change_current_webcam(self, index):
        if self.is_invalid_index(index):
            return ''
        self.webcam_port = index
        return self.video_capture.change(index)
    

    def is_invalid_index(self, index):
        return index is None or (type(index) is not int) or index < 0


    def generate(self):
        try:
            FRAME_RATE, previous = 0.1, 0
            while True:
                img = self.get_image()
                if (time.time() - previous) > (FRAME_RATE):
                    previous = time.time()
                    yield(b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
        except:
            pass
    

    def get_image(self):
        try:
            if(self.has_uploaded_image()):
                return self.get_uploaded_image()
            return self.get_webcam_image()
        except:
            return MyOpencv.convert_to_bytes(MyOpencv.black_image())
    

    def has_uploaded_image(self):
        with self.lock_uploaded_image:
            return MyOpencv.validate_image(self.uploaded_image)
    

    def get_uploaded_image(self):
        with self.lock_uploaded_image:
            copy = self.uploaded_image.copy()
        drawed_immage = self.rectangle.draw_rectangle(copy)
        return MyOpencv.convert_to_bytes(drawed_immage)
    

    def get_webcam_image(self):
        frame = self.video_capture.capture_frame()
        self.set_output_frame(frame.copy())
        drawed_immage = self.rectangle.draw_rectangle(frame)
        return MyOpencv.convert_to_bytes(drawed_immage)


    def set_output_frame(self, frame):
        with self.lock_frame:
            self.output_frame = frame


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
        try:
            self._save_uploaded_image(image)
        except:
            return ''
    

    def _save_uploaded_image(self, image):
        if image:
            new_image = MyOpencv.convert_and_resize_image(image, self.get_frame_shape())
            self.set_uploaded_image(new_image)
    

    def set_uploaded_image(self, image):
        with self.lock_uploaded_image:
                self.uploaded_image = image
    

    def clear_rectangle_and_uploaded_image(self):
        self.rectangle.initial_points_of_rectangle()
        self.set_uploaded_image(None)
    

    def clear(self):
        self.turn_off_webcam()
        self.clear_rectangle_and_uploaded_image()
    

    def turn_off_webcam(self):
        self.video_capture.turn_off()
    

    def __del__(self):
        self.turn_off_webcam()

