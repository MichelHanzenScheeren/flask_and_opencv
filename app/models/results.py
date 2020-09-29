from app.models.image_pack import ImagePack
from app.models.excel_file import ExcelFile
from datetime import datetime
from base64 import b64encode
from pyzip import PyZip


class Results():
    def __init__(self):
        self.differentiator = []
        self.captures = [] 
        self.signals = []
        self.captures_images = []
        self.differentiator_image = None
    

    def initialize(self, total_time, captures_seg, description):
        self.initial_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)
        self.description = description or ""
        self.captures.clear()
        self.signals.clear()
        self.captures_images.clear()


    def get_differentiator_image(self):
        try:
            jpg_image = image_pack.encode_to_jpg(self.differentiator_image)
            return b64encode(jpg_image)
        except:
            return ''


    def get_all_images(self):
        try:
            return self.encode_all_images()
        except:
            return ''


    def encode_all_images(self):
        encoded = PyZip()
        encoded["diferenciador.jpg"] = image_pack.convert_to_bytes(self.differentiator_image)
        for i in range(0, len(self.captures_images)):
            image = self.captures_images[i]
            encoded[f"captura_{i + 1}.jpg"] = image_pack.convert_to_bytes(image)
        return b64encode(encoded.to_bytes())


    def get_xlsx_results(self):
        try:
            file = ExcelFile(title = "Resultados")
            return file.create(self.general_info(), self.differentiator_info(), self.captures_info())
        except:
            return ''
    

    def general_info(self):
        title = ["Informações Gerais", "", "", "", ""]
        headers = ["Data", "Duração", "Capturas", "Total", "Descrição"]
        content = [self.initial_date, f"{self.total_time} segundos", f"{self.captures_seg} cap./seg."]
        content.extend([f"{self.total_time * self.captures_seg} cap.",  f"{self.description or 'Não informada'}"])
        return [title, headers, content]
    

    def differentiator_info(self):
        title = ["Diferenciador", "", ""]
        headers = ["Vermelho", "Verde", "Azul"]
        content = [self.differentiator[2], self.differentiator[1], self.differentiator[0]]
        return [title, headers, content]
    

    def captures_info(self):
        title = ["Capturas", "", "", "", ""]
        table_headers = ["Tempo (segundos)", "Vermelho", "Verde", "Azul", "Sinal"]
        information = [title, table_headers]
        for i, value in enumerate(self.captures):
            new_data = [(i + 1) * self.interval, value[2], value[1], value[0], self.signals[i]]
            information.append(new_data)
        return information


