from threading import Lock
from app.models.image_pack import ImagePack


class Frame:
    def __init__(self):
        self._frame = None
        self._lock = Lock()
    

    def set_frame(self, new_frame):
        with self._lock:
            self._frame = new_frame
    

    def get_copy(self):
        with self._lock:
            if self._frame is None:
                return None
            return self._frame.copy()


    def is_valid(self):
        with self._lock:
            return ImagePack.validate_image(self._frame)
    

    def clear(self):
        with self._lock:
            self._frame = None