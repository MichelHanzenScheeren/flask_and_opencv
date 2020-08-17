from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font
from io import BytesIO
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
        encoded["diferenciador.jpg"] = self.encode_image(self.differentiator_image, webcam)
        for i in range(0, len(self.captures_images)):
            image = self.captures_images[i]
            encoded[f"captura_{i + 1}.jpg"] = self.encode_image(image, webcam)
        return json.dumps(encoded)


    def encode_image(self, image, webcam):
        jpg_image = webcam.encode_to_jpg(image)
        return f"{base64.b64encode(jpg_image)}"
    

    def get_xlsx_results(self):
        excel_file = Workbook()
        spreadsheet1 = excel_file.active
        spreadsheet1.title = "Resultados"
        font1 = Font(name='Arial', size=12)

        general_information = self.get_general_information()
        for index, information in enumerate(general_information):
            for position, column in enumerate(information):
                spreadsheet1.cell(row = index + 1, column = position + 1).font = font1
                spreadsheet1.cell(row = index + 1, column = position + 1, value = column)
        
        for column in spreadsheet1.columns:
            length = max(len(str(cell.value)) for cell in column)
            spreadsheet1.column_dimensions[column[0].column_letter].width = length * 1.2
        
        encoded = BytesIO()
        excel_file.save(encoded)
        encoded.seek(0)
        base_64 = base64.b64encode(encoded.read())
        return base_64
    

    def get_general_information(self):
        init = ["Início da análise", self.initial_date]
        duration = ["Duração", f"{self.total_time}"]
        captures = ["Capturas", f"{self.captures_seg}"]
        total = ["Total de capturas", f"{self.total_time * self.captures_seg}"]
        descript = ["Descrição", f"{self.description}"]
        return [init, duration, captures, total, descript]
        

