from time import sleep
from math import sqrt, pow
from app.models.results import Results


class Analyze():
    def __init__(self):
        self.results = Results()
    

    def get_differentiator(self, webcam):
        try:
            return self._get_differentiator(webcam)
        except:
            return ''
    

    def _get_differentiator(self, webcam):
        image = webcam.get_differentiator_image()
        self.results.differentiator_image = image
        result = self.calculate_average(image)
        self.results.differentiator = result
        return f'[{result[2]:.3f}, {result[1]:.3f}, {result[0]:.3f}]'


    def calculate_average(self, image):
        return image.mean(axis=0).mean(axis=0)


    def start_analyze(self, total_time, captures_seg, description, webcam):
        if (total_time.isdigit() and captures_seg.isdigit()):
            self.results.initialize(int(total_time), int(captures_seg), description)
            self.save_analyze_frames(webcam)
            self.do_analyze()
            self.calculate_signal()
            webcam.clear()
    

    def save_analyze_frames(self, webcam):
        repetitions = int(self.results.total_time * self.results.captures_seg)
        for _ in range(0, repetitions):
            image = webcam.selected_rectangle_image()
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
    
