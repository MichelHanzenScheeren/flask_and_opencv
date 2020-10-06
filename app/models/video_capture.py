from threading import Lock
from app.models.image_pack import ImagePack

class VideoCapture:
  def __init__(self):
    self._is_working = True
    self.video_capture = None
    self.lock_video = Lock()
  

  def start_video(self, port):
    if not self.is_valid() or not self.is_working():
      self.start_video_stream(port)
      self.define_resolution()
      self.set_working_state(True)
  

  def is_valid(self):
    with self.lock_video:
      return self.video_capture and self.video_capture.isOpened()
  

  def is_working(self):
    with self.lock_video:
      return self._is_working
  

  def start_video_stream(self, port):
    with self.lock_video:
      self.video_capture = ImagePack.new_stream(port)


  def define_resolution(self):
    with self.lock_video:
      if(self.video_capture.get(3) != 640 or self.video_capture.get(4) != 480):
        self.video_capture.set(3, 640)
        self.video_capture.set(4, 480)
  

  def set_working_state(self, condition = True):
    with self.lock_video:
      self._is_working = condition
  

  def video_status(self):
    if not self.is_valid():
      h, w, success = (480, 640, False)
      self.set_working_state(False)
    else:
      h, w = self.get_video_dimensions()
      _ = self.capture_frame() # Necessário para verificação do funcionamento
      success = self.is_working()
    return (h, w, success)
  

  def get_video_dimensions(self):
    with self.lock_video:
      return (int(self.video_capture.get(4)), int(self.video_capture.get(3)))
  

  def capture_frame(self):
    if(self.is_working() and self.is_valid()):
      return self._do_capture()
    return ImagePack.black_image()
  

  def _do_capture(self):
    with self.lock_video:
      success, frame = self.video_capture.read()
    self.set_working_state(success)
    return frame if success else ImagePack.black_image()


  def change(self, new_port):
    try:
      _change_video(new_port)
    except:
      return ''
  

  def _change_video(self, new_port):
    with self.lock_video:
      to_free = self.video_capture
      self.video_capture = None
    self.start_video(new_port)
    to_free.release()
    return self.video_status()
  

  def turn_off(self):
    with self.lock_video:
      if self.video_capture:
        self.video_capture.release()
        self.video_capture = None
