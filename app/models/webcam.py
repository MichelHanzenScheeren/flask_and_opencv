import time
from app.models.rectangle import Rectangle
from app.models.video_capture import VideoCapture
from app.models.my_opencv import MyOpencv
from app.models.frame import Frame


class Webcam():
    def __init__(self):
        self.current_port = 0
        self.rectangle = Rectangle()
        self.video_capture = VideoCapture()
        self.captured_frame = Frame()
        self.uploaded_frame = Frame()
    

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
            if(self.uploaded_frame.is_valid()):
                copy = self.uploaded_frame.get_copy()
            else:
                copy = self.get_webcam_image()
            return self.draw_and_convert_frame(copy)
        except:
            return MyOpencv.convert_to_bytes(MyOpencv.black_image())
    

    def get_webcam_image(self):
        frame = self.video_capture.capture_frame()
        self.captured_frame.set_frame(frame.copy())
        return frame
    

    def draw_and_convert_frame(self, copy):
        drawed_immage = self.rectangle.draw_rectangle(copy)
        return MyOpencv.convert_to_bytes(drawed_immage)


    def get_differentiator_image(self):
        if(self.uploaded_frame.is_valid()):
            return self.crop_uploaded_image()
        return self.selected_rectangle_image()
    

    def crop_uploaded_image(self):
        copy = self.uploaded_frame.get_copy()
        self.uploaded_frame.clear()
        return self.rectangle.crop_image(copy)


    def selected_rectangle_image(self):
        copy = self.captured_frame.get_copy()
        return self.rectangle.crop_image(copy)
    

    def save_uploaded_image(self, image):
        try:
            self._save_uploaded_image(image)
        except:
            return ''
    

    def _save_uploaded_image(self, image):
        if image is None:
            return
        frame = MyOpencv.convert_to_frame(image)
        new_image = MyOpencv.resize_image(frame, self.video_capture.get_video_dimensions())
        self.uploaded_frame.set_frame(new_image)
    

    def clear_rectangle_and_uploaded_image(self):
        self.rectangle.initial_points_of_rectangle()
        self.uploaded_frame.clear()
    

    def clear(self):
        self.turn_off_webcam()
        self.clear_rectangle_and_uploaded_image()
    

    def turn_off_webcam(self):
        self.video_capture.turn_off()
    

    def __del__(self):
        self.turn_off_webcam()

