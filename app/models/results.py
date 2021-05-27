from app.models.image_pack import ImagePack
from app.models.excel_file import ExcelFile
from datetime import datetime
from base64 import b64encode
from pyzip import PyZip


class Results():
    """ Classe criada para encapsular todos os resultados da análise para que sejam enviados ao front-end. 

    Também é responsável por recuperar e formatar imagens da análise, bem como criar o arquivo xlsx.
    """

    def __init__(self):
        # Armazena a lista BGR [Blue, Green, Red] correspondente a média de cores da imagem do diferenciador.
        self.differentiator = []
        # Lista de listas dos resultados da média de cores das capturas [[Blue, Green, Red], [Blue, ...], ...].
        self.captures = []
        self.signals = []  # Lista de sinais obtidos na análise. [sinal1, sinal2, ...].
        self.captures_images = []  # Lista de imagens das capturas.
        self.differentiator_image = None  # imagenm do diferenciador.

    def initialize(self, total_time, captures_seg, description, select_date, user_date):
        """ Salva os primeiros valores da análise e garante que dados de uma análise anterior sejam limpos. """
        if(select_date == 'user'):
            self.initial_date = datetime.strptime(
                user_date, '%d-%m-%Y %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
        else:
            self.initial_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)
        self.description = description or ""
        self.captures.clear()
        self.signals.clear()
        self.captures_images.clear()

    def get_differentiator_image(self):
        """ Recupera a imagem do diferenciador e a formata para ser retornada ao front-end. 

        Se nenhum erro ocorrer, retorna uma imagem em formato JPG codificada em bytes na base64.
        Se um erro ocorrer, retorna uma string vazia.
        """
        try:
            jpg_image = ImagePack.encode_to_jpg(self.differentiator_image)
            return b64encode(jpg_image)
        except:
            return ''

    def get_all_images(self):
        """ Recupera as imagens das capturas e as formata para serem retornadas ao front-end. 

        Se nenhum erro ocorrer, retorna um json com imagens em formato JPG codificadas em bytes na base64.
        Se um erro ocorrer, retorna uma string vazia.
        """
        try:
            return self.encode_all_images()
        except:
            return ''

    def encode_all_images(self):
        encoded = PyZip()
        encoded['diferenciador.jpg'] = ImagePack.convert_to_bytes(self.differentiator_image)
        for i in range(0, len(self.captures_images)):
            image = self.captures_images[i]
            encoded[f'captura_{i + 1}.jpg'] = ImagePack.convert_to_bytes(image)
        return b64encode(encoded.to_bytes())

    def get_xlsx_results(self):
        """ Cria e retorna um arquivo xlsx com os resultados da análise. """
        try:
            file = ExcelFile(title='Resultados')
            return file.create(self.general_info(), self.differentiator_info(), self.captures_info())
        except:
            return ''

    def general_info(self):
        """ Reúne e retorna uma lista de listas com titulos e informações gerais da análise. """
        title = ['Informações Gerais', '', '', '', '']
        headers = ['Data', 'Duração', 'Capturas', 'Total', 'Descrição']
        content = [self.initial_date, f'{self.total_time} segundos', f'{self.captures_seg} cap./seg.']
        content.extend([f'{self.total_time * self.captures_seg} cap.', f'{self.description or "Não informada"}'])
        return [title, headers, content]

    def differentiator_info(self):
        """ Reúne titulos e os resultados do diferenciador em uma lista de listas. """
        title = ['Diferenciador', '', '']
        headers = ['Vermelho', 'Verde', 'Azul']
        content = [self.differentiator[2], self.differentiator[1], self.differentiator[0]]
        return [title, headers, content]

    def captures_info(self):
        """ Reúne titulos e os resultados das capturas em uma lista de listas. """
        title = ['Capturas', '', '', '', '', '']
        header = ['Nº Captura', 'Tempo (segundos)', 'Vermelho', 'Verde', 'Azul', 'Sinal']
        information = [title, header]
        for i, value in enumerate(self.captures):
            row = [i+1, (i+1)*self.interval, value[2], value[1], value[0], self.signals[i]]
            information.append(row)
        return information

    def saveNewAnalyzeDate(self, newDate):
        try:
            self.initial_date = datetime.strptime(newDate, '%d-%m-%Y %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')
            return ''
        except:
            return 'Formato Inválido'
