from app.models.rectangle import Rectangle
from app.models.video_capture import VideoCapture
from app.models.image_pack import ImagePack
from app.models.frame import Frame
from time import sleep


class Webcam():
  def __init__(self):
    self.current_port = 0
    self.rectangle = Rectangle()
    self.uploaded_frame = Frame()
    self.captured_frame = Frame()
    self.video_capture = VideoCapture(self.captured_frame.set_frame)


  def init_webcam(self):
    self.video_capture.start_video(self.current_port)
  

  def video_status_and_port(self):
    status = self.video_capture.video_status()
    status['current'] = self.current_port
    return status
  

  def webcans_list(self):
    list_webcans = []
    for index in range(100):
      if index == self.current_port:
        continue
      if not ImagePack.is_valid_webcam(index):
        break
      list_webcans.append(index)
    list_webcans.insert(self.current_port, self.current_port)
    return list_webcans


  def change_current_webcam(self, index):
    if self.is_invalid_index(index):
      return ''
    self.current_port = index
    return self.video_capture.change(index)
  

  def is_invalid_index(self, index):
    return index is None or (type(index) is not int) or index < 0


  def stream_webcam(self):
    try:
      while True:
        img = self.get_image()
        yield(b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
        sleep(0.04)
    except Exception as exception:
      print(exception)
  

  def get_image(self):
    try:
      if(self.uploaded_frame.is_valid()):
        copy = self.uploaded_frame.get_copy()
      else:
        copy = self.captured_frame.get_copy()
      return self.draw_and_convert_frame(copy)
    except:
      return ImagePack.convert_to_bytes(ImagePack.black_image())


  def draw_and_convert_frame(self, copy):
    drawed_image = self.rectangle.draw_rectangle(copy)
    return ImagePack.convert_to_bytes(drawed_image)


  def get_differentiator_image(self):
    if(self.uploaded_frame.is_valid()):
      return self.crop_uploaded_image()
    return self.get_cropped_image()
  

  def crop_uploaded_image(self):
    copy = self.uploaded_frame.get_copy()
    self.uploaded_frame.clear()
    return self.rectangle.crop_image(copy)


  def get_cropped_image(self):
    copy = self.captured_frame.get_copy()
    return self.rectangle.crop_image(copy)
  

  def save_uploaded_image(self, image):
    try:
      self._save_uploaded_image(image)
    except:
      return ''
  

  def _save_uploaded_image(self, image):
    frame = ImagePack.convert_to_frame(image)
    video_dimensions = self.video_capture.get_video_dimensions()
    new_image = ImagePack.resize_image(frame, video_dimensions)
    self.uploaded_frame.set_frame(new_image)
  

  def clear_rectangle_and_uploaded_image(self):
    self.rectangle.initial_points_of_rectangle()
    self.uploaded_frame.clear()
  

  def clear(self):
    self.video_capture.turn_off()
    self.clear_rectangle_and_uploaded_image()
  

  def __del__(self):
    self.video_capture.turn_off()
    self.clear_rectangle_and_uploaded_image()

