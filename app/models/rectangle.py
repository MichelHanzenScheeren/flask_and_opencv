from threading import Lock
import cv2.cv2 as cv2

class Rectangle():
    def __init__(self):
        self.x_initial = -1
        self.y_initial = -1
        self.x_final = -1
        self.y_final = -1
        self.lock_drawing = Lock()


    def get_measures(self, x1, y1, x2, y2):
        with self.lock_drawing:
            if x1 and y1 and x2 and y2:
                self.x_initial = x1
                self.y_initial = y1
                self.x_final = x2
                self.y_final = y2

    def draw_rectangle(self, frame):
        with self.lock_drawing:
            if self.x_initial != -1 and self.x_final != -1:
                cv2.rectangle(frame, (self.x_initial, self.y_initial), (self.x_final, self.y_final), (0, 0, 255), 1)
        return frame

"""
    x_initial __________________
    y_initial                   |
     |                          |
     |                          |
     |                          |
     |                          |
     |_________________________  x_final
                                 y_final      
"""