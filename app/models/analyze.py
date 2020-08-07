from time import sleep
from math import sqrt, pow
from app.models.results import Results

class Analyze():
    def __init__(self):
        self.differentiator = []
        self.results = Results()

    def get_differentiator(self, webcam):
        self.differentiator = (webcam.get_differentiator_image().mean(axis=0).mean(axis=0))
        return f'[{self.differentiator[2]:.3f}, {self.differentiator[1]:.3f}, {self.differentiator[0]:.3f}]'

    def start_analyze(self, total_time, captures_seg, webcam):
        self.initialize_parameters(total_time, captures_seg)
        self.do_analyze(webcam)
        self.calculate_signal()
        self.save_results()
    

    def initialize_parameters(self, total_time, captures_seg):
        self.captures = []
        self.signals = []
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)
    

    def do_analyze(self, webcam):
        repetitions = int(self.total_time * self.captures_seg)
        for _ in range(0, repetitions + 1):
            self.captures.append(webcam.selected_rectangle_image().mean(axis=0).mean(axis=0))
            sleep(self.interval)


    def calculate_signal(self):
        for capture in self.captures:
            signal = sqrt(
                pow(capture[0] - self.differentiator[0], 2) +
                pow(capture[1] - self.differentiator[1], 2) +
                pow(capture[2] - self.differentiator[2], 2)
            )
            self.signals.append(signal)
    

    def save_results(self):
        self.results.save_results(
            differentiator = self.differentiator,
            captures = self.captures,
            signals = self.signals,
            total_time = self.total_time,
            captures_seg = self.captures_seg,
            interval = self.interval
        )