from time import sleep
from math import sqrt, pow
import base64
import json
from app.models.results import Results

import zipfile
import io


class Analyze():
    def __init__(self):
        self.results = Results()
        

    def get_differentiator(self, webcam):
        image = webcam.get_differentiator_image()
        self.results.differentiator_image = image
        result = self.calculate_average(image)
        self.results.differentiator = result
        return f'[{result[2]:.3f}, {result[1]:.3f}, {result[0]:.3f}]'
    

    def get_differentiator_image(self, webcam):
        jpg_image = webcam.encode_to_jpg(self.results.differentiator_image)
        my_encoded_img = base64.b64encode(jpg_image)
        return my_encoded_img
    

    # def get_zip_images(self, webcam):
    #     encoded_images = {}
    #     for i in range(0, len(self.results.captures_images)):
    #         image = self.results.captures_images[i]
    #         encoded_images[f"captura_{i}"] = f"{self.generate_encoded_image(image, webcam)}"
    #     return json.dumps(encoded_images)
    

    # def generate_encoded_image(self, image, webcam):
    #     jpg_image = webcam.encode_to_jpg(image)
    #     return base64.b64encode(jpg_image)

    def get_zip_images(self, webcam):
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for i in range(0, len(self.results.captures_images)):
                data = zipfile.ZipInfo(f"captura_{i + 1}.jpg")
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, webcam.encode_to_jpg(self.results.captures_images[i]))
        memory_file.seek(0)
        return memory_file
    

    def calculate_average(self, image):
        return image.mean(axis=0).mean(axis=0)


    def start_analyze(self, total_time, captures_seg, description, webcam):
        if not (total_time.isdigit() and captures_seg.isdigit()):
            return
        self.results.initialize_parameters(int(total_time), int(captures_seg), description)
        self.do_analyze(webcam)
        self.calculate_signal()
    

    def do_analyze(self, webcam):
        repetitions = int(self.results.total_time * self.results.captures_seg)
        for _ in range(0, repetitions):
            image = webcam.selected_rectangle_image()
            self.results.captures_images.append(image)
            self.results.captures.append(self.calculate_average(image))
            sleep(self.results.interval)


    def calculate_signal(self):
        differentiator = self.results.differentiator
        for capture in self.results.captures:
            signal = sqrt(
                pow(capture[0] - differentiator[0], 2) +
                pow(capture[1] - differentiator[1], 2) +
                pow(capture[2] - differentiator[2], 2)
            )
            self.results.signals.append(signal)
    

    def is_valid(self): 
        return len(self.results.differentiator) > 0 and len(self.results.captures) > 0
    


    

