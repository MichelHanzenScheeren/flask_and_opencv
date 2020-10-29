from time import sleep
from math import sqrt, pow
from app.models.results import Results


class Analyze():
  def __init__(self):
    self.results = Results()
  

  def calculate_differentiator(self, get_differentiator_image):
    try:
      return self._calculate_differentiator(get_differentiator_image)
    except Exception as exception:
      print(exception)
      return ''
  

  def _calculate_differentiator(self, get_differentiator_image):
    image = get_differentiator_image()
    self.results.differentiator_image = image
    result = self.calculate_average(image)
    self.results.differentiator = result
    return f'[{result[2]:.3f}, {result[1]:.3f}, {result[0]:.3f}]'


  def calculate_average(self, image):
    return image.mean(axis=0).mean(axis=0)


  def start_analyze(self, total_time, captures_seg, description, get_cropped_image):
    if (self.form_is_valid(total_time, captures_seg)):
      self.results.initialize(int(total_time), int(captures_seg), description)
      self.save_analyze_frames(get_cropped_image)
      self.do_analyze()
      self.calculate_signal()
    else:
      raise Exception('Formulário inválido!')
  

  def form_is_valid(self, time, captures):
    is_digit = time.isdigit() and captures.isdigit()
    valid_range = int(time) >= 1 and int(captures) >= 1 and int(captures) <= 10
    return is_digit and valid_range


  def save_analyze_frames(self, get_cropped_image):
    repetitions = int(self.results.total_time * self.results.captures_seg)
    for _ in range(0, repetitions):
      image = get_cropped_image()
      self.results.captures_images.append(image)
      sleep(self.results.interval)


  def do_analyze(self):
    for image in self.results.captures_images:
      average = self.calculate_average(image)
      self.results.captures.append(average)


  def calculate_signal(self):
    differentiator = self.results.differentiator
    for capture in self.results.captures:
      signal = sqrt(
          pow(capture[0] - differentiator[0], 2) +
          pow(capture[1] - differentiator[1], 2) +
          pow(capture[2] - differentiator[2], 2)
      )
      self.results.signals.append(signal)
  

  def clear(self): 
    if len(self.results.differentiator) != 0:
      self.results = Results()
    
