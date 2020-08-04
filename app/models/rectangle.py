from threading import Lock
import cv2.cv2 as cv2

class Rectangle():
    def __init__(self):
        self.x_initial = 0
        self.y_initial = 0
        self.x_final = 0
        self.y_final = 0
        self.lock_drawing = Lock()


    def get_measures(self, x1, y1, x2, y2):
        with self.lock_drawing:
            if x1 and y1 and x2 and y2:
                self.x_initial = min(x1, x2)
                self.y_initial = min(y1, y2)
                self.x_final = self.x_initial + abs(x1 - x2)
                self.y_final = self.y_initial + abs(y1 - y2)


    def draw_rectangle(self, frame):
        with self.lock_drawing:
            if (self.x_initial != 0 or self.x_final != 0) and (self.y_initial != 0 or self.y_final):
                cv2.rectangle(frame, (self.x_initial, self.y_initial), (self.x_final, self.y_final), (0, 0, 255), 1)
        return frame


    def clear(self):
        self.y_initial = 0
        self.x_initial = 0
        self.x_final = 0
        self.y_final = 0