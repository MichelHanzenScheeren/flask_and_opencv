from threading import Lock
from app.models.image_pack import ImagePack

class Rectangle():
    def __init__(self):
        self.lock_drawing = Lock()
        self.initial_points_of_rectangle()
        
    
    def initial_points_of_rectangle(self):
        with self.lock_drawing:
            self.x_initial = 0
            self.y_initial = 0
            self.x_final = 0
            self.y_final = 0


    def define_points_of_rectangle(self, x1, y1, x2, y2):
        with self.lock_drawing:
            if self.is_int(x1, y1, x2, y2) and self.is_valid_points(x1, y1, x2, y2):
                self.x_initial = min(x1, x2)
                self.y_initial = min(y1, y2)
                self.x_final = self.x_initial + abs(x1 - x2)
                self.y_final = self.y_initial + abs(y1 - y2)
    

    def is_int(self, x1, y1, x2, y2):
        return (type(x1) is int) and (type(y1) is int) and (type(x2) is int) and (type(y2) is int)
    

    def is_valid_points(self, x1, y1, x2, y2):
        greater_than_zero = (x1 >= 0) and (y1 >= 0) and (x2 >= 0) and (y2 >= 0)
        has_area = ((x1 - x2) != 0) and ((y1 - y2) != 0)
        return (greater_than_zero and has_area)


    def is_valid_rectangle(self):
        with self.lock_drawing:
            return ((self.x_initial != 0 or self.x_final != 0) 
            and (self.y_initial != 0 or self.y_final))
    

    def draw_rectangle(self, frame):
        if self.is_valid_rectangle():
            ImagePack.draw_rectangle(frame, self.initial_xy(), self.final_xy())
        return frame


    def initial_xy(self):
        with self.lock_drawing:
            return (self.x_initial, self.y_initial)


    def final_xy(self):
        with self.lock_drawing:
            return (self.x_final, self.y_final)


    def crop_image(self, image):
        if(self.is_valid_rectangle()):
            with self.lock_drawing:
                return image[self.y_initial:self.y_final, self.x_initial:self.x_final]
        return image
