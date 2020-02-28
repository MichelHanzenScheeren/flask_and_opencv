class Analyze():
    def __init__(self):
        self.differentiator = 0

    def get_differentiator(self, webcam, rectangle):
        while True:
            with webcam.lock_frame:
                frame = webcam.output_frame.copy()
            if frame is None:
                continue
            with rectangle.lock_drawing:
                self.differentiator = (frame[rectangle.y_initial:rectangle.y_final, rectangle.x_initial:rectangle.x_final].mean(axis=0).mean(axis=0))
                return f'[{self.differentiator[2]:.3f}, {self.differentiator[1]:.3f}, {self.differentiator[0]:.3f}]'