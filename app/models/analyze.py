from time import sleep
from math import sqrt, pow

class Analyze():
    def __init__(self):
        self.differentiator = []
        self.total_time = 0
        self.captures_seg = 0

    def get_differentiator(self, webcam, rectangle):
        while True:
            with webcam.lock_frame:
                frame = webcam.output_frame.copy()
            if frame is None:
                continue
            with rectangle.lock_drawing:
                self.differentiator = (frame[rectangle.y_initial:rectangle.y_final, rectangle.x_initial:rectangle.x_final].mean(axis=0).mean(axis=0))
                return f'[{self.differentiator[2]:.3f}, {self.differentiator[1]:.3f}, {self.differentiator[0]:.3f}]'

    def start_analyze(self, total_time, captures_seg, webcam, rectangle):
        self.captures = []
        self.signals = []
        self.total_time = total_time
        self.captures_seg = captures_seg
        repetitions = int(total_time * captures_seg)
        interval = 1 / captures_seg
        for i in range(0,repetitions):
            with webcam.lock_frame:
                frame = webcam.output_frame.copy()
            if frame is None:
                continue
            with rectangle.lock_drawing:
                self.captures.append((frame[rectangle.y_initial:rectangle.y_final, rectangle.x_initial:rectangle.x_final].mean(axis=0).mean(axis=0)))
            sleep(interval)
        self.calculate_signal()

    def calculate_signal(self):
        for capture in self.captures:
            self.signals.append(sqrt(pow(capture[0] - self.differentiator[0], 2) +
                                     pow(capture[1] - self.differentiator[1], 2) +
                                     pow(capture[2] - self.differentiator[2], 2)))