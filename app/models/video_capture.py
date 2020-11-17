import time
from threading import Lock, Thread
from app.models.image_pack import ImagePack

class VideoCapture:
  def __init__(self, set_frame):
    self.set_frame = set_frame
    self._is_working = True
    self.video_capture = None
    self.lock_video = Lock()
    self.thread = None
  

  def start_video(self, port):
    if not self.is_working() or not self.is_valid():
      self.start_video_stream(port)
      self.set_working_state(True)
      self.start_thread()
      self.define_resolution()
  

  def is_valid(self):
    with self.lock_video:
      return self.video_capture and self.video_capture.isOpened()
  

  def is_working(self):
    with self.lock_video:
      return self._is_working
  

  def start_video_stream(self, port):
    with self.lock_video:
      self.video_capture = ImagePack.new_stream(port)
  

  def start_thread(self):
    self.thread = Thread(target=self.capture_webcam_image, daemon=True)
    self.thread.start()
  

  def capture_webcam_image(self):
    try:
      FRAME_RATE, previous = 0.04, 0
      while self.is_working():
        if (time.time() - previous) >= FRAME_RATE:
          frame = self.capture_frame()
          self.set_frame(frame)
          previous = time.time()
    except Exception as erro:
      print(erro)
  

  def define_resolution(self):
    with self.lock_video:
      if(self.video_capture.get(3) != 640 or self.video_capture.get(4) != 480):
        self.video_capture.set(3, 640)
        self.video_capture.set(4, 480)
      print(f'\nRESOLUÇÃO: {self.video_capture.get(4):.0f}X{self.video_capture.get(3):.0f}')
  

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
    return {'style': f'height:{h}px;min-height:{h}px;width:{w}px;min-width:{w}px;',
        'success': success}
  

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
      with self.lock_video:
        to_dispose = self.video_capture
        self.video_capture = ImagePack.new_stream(new_port)
        self._is_working = True
      self.define_resolution()
      to_dispose.release()
      return self.video_status()
    except:
      return ''


  def turn_off(self):
    self.set_working_state(False)
    with self.lock_video:
      if self.video_capture:
        self.video_capture.release()
        self.video_capture = None
    self.thread = None

