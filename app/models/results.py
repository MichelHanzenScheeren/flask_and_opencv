from datetime import datetime
import base64
import json


class Results():
    def __init__(self):
        self.differentiator = []
        self.captures = [] 
        self.signals = []
        self.captures_images = []
        self.differentiator_image = None
    

    def initialize_parameters(self, total_time, captures_seg, description):
        self.initial_date = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)
        self.description = description or ""
        self.captures.clear()
        self.signals.clear()
        self.captures_images.clear()
    

    def get_differentiator_image(self, webcam):
        if self.differentiator_image is None:
            return "" 
        jpg_image = webcam.encode_to_jpg(self.differentiator_image)
        return base64.b64encode(jpg_image)


    def get_zip_images(self, webcam):
        encoded = {}
        encoded["differentiator.jpg"] = self.encode_image(self.differentiator_image, webcam)
        for i in range(0, len(self.captures_images)):
            image = self.captures_images[i]
            encoded[f"capture_{i + 1}.jpg"] = self.encode_image(image, webcam)
        return json.dumps(encoded)


    def encode_image(self, image, webcam):
        jpg_image = webcam.encode_to_jpg(image)
        return f"{base64.b64encode(jpg_image)}"
