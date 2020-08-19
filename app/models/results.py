from app.models.excel_file import Excel_File
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
        self.initial_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)
        self.description = description or ""
        self.captures.clear()
        self.signals.clear()
        self.captures_images.clear()
    

    def get_differentiator_image(self, webcam):
        try:
            return self.encode_image(self.differentiator_image, webcam)
        except:
            return ''


    def get_all_images(self, webcam):
        try:
            return self.encode_all_images(webcam)
        except:
            return ''
    

    def encode_all_images(self, webcam):
        encoded = {}
        encoded["diferenciador.jpg"] = f"{self.encode_image(self.differentiator_image, webcam)}"
        for i in range(0, len(self.captures_images)):
            image = self.captures_images[i]
            encoded[f"captura_{i + 1}.jpg"] = f"{self.encode_image(image, webcam)}"
        return json.dumps(encoded)


    def encode_image(self, image, webcam):
        jpg_image = webcam.encode_to_jpg(image)
        return base64.b64encode(jpg_image)
    

    def get_xlsx_results(self):
        try:
            file = Excel_File(title = "Resultados")
            return file.build_file(self.general_info(), self.differentiator_info(), self.captures_info())
        except:
            return ''
    

    def general_info(self):
        title = ["Informações Gerais", "", "", "", ""]
        table_headers = ["Data", "Duração", "Capturas", "Total", "Descrição"]
        table_content = [self.initial_date, f"{self.total_time} segundos", f"{self.captures_seg} cap./seg."]
        table_content.extend([f"{self.total_time * self.captures_seg} cap.",  f"{self.description or 'Não informada'}"])
        return [title, table_headers, table_content]
    

    def differentiator_info(self):
        title = ["Diferenciador", "", ""]
        table_headers = ["Vermelho", "Verde", "Azul"]
        table_content = [self.differentiator[2], self.differentiator[1], self.differentiator[0]]
        return [title, table_headers, table_content]
    

    def captures_info(self):
        title = ["Capturas", "", "", "", ""]
        table_headers = ["Tempo (segundos)", "Vermelho", "Verde", "Azul", "Sinal"]
        information = [title, table_headers]
        for index, value in enumerate(self.captures):
            new_data = [(index + 1) * self.interval, value[2], value[1], value[0], self.signals[index]]
            information.append(new_data)
        return information


