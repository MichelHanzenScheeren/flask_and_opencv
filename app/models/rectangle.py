from threading import Lock
import cv2.cv2 as cv2

class Rectangle():
    def __init__(self):
        self.lock_drawing = Lock()
        self.initial_points_of_rectangle()
        
    
    def initial_points_of_rectangle(self):
        self.x_initial = 0
        self.y_initial = 0
        self.x_final = 0
        self.y_final = 0


    def define_points_of_rectangle(self, x1, y1, x2, y2):
        with self.lock_drawing:
            if x1 and y1 and x2 and y2:
                self.x_initial = min(x1, x2)
                self.y_initial = min(y1, y2)
                self.x_final = self.x_initial + abs(x1 - x2)
                self.y_final = self.y_initial + abs(y1 - y2)


    def is_valid_rectangle(self):
        with self.lock_drawing:
            return ((self.x_initial != 0 or self.x_final != 0) 
            and (self.y_initial != 0 or self.y_final))


    def initial_xy(self):
        with self.lock_drawing:
            return (self.x_initial, self.y_initial)


    def final_xy(self):
        with self.lock_drawing:
            return (self.x_final, self.y_final)


    def crop_image(self, image):
        return image[self.y_initial:self.y_final, self.x_initial:self.x_final]
