from datetime import datetime
from app.configuration import STRING_FORMAT
from app.domain.packs.image_pack import ImagePack
from app.domain.models.excel_file import ExcelFile


class Results():
    """ Classe criada para encapsular todos os resultados da análise para que sejam enviados ao front-end.
    Também é responsável por recuperar e formatar imagens da análise, bem como criar o arquivo xlsx.
    """

    def __init__(self):
        self.differentiator = [-1, -1, -1]  # Lista BGR [Blue, Green, Red] da média de cores da imagem do diferenciador.
        self.differentiator_image = None  # imagem do diferenciador.
        self.total_time = 10
        self.captures_seg = 1
        self.refresh_data()

    def refresh_data(self):
        self.captures = []  # Matriz de resultados da média de cores das capturas [[B, G, R], [B, ...], ...].
        self.captures_images = ImagePack.create_zip_file()  # dicionário de imagens das capturas para exportar em zip.
        self.captures_times = []  # Lista de datetimes que representam o instante em que a captura foi feita
        self.signals = []  # Lista de sinais obtidos na análise. [sinal1, sinal2, ...].
        self.calibration_values = []  # Lista de coordenadas y do gráfico de calibração da analise.
        self.encoded_images = None  # Armazena as imagens convertidas para envio ao front.

    def initialize(self, analyze_method, total_time, captures_seg, description, select_date, user_date):
        """ Salva os primeiros valores da análise e garante que dados de uma análise anterior sejam limpos. """
        if(select_date == 'user'):
            self.initial_date = datetime.strptime(user_date, STRING_FORMAT).strftime(STRING_FORMAT)
        else:
            self.initial_date = datetime.now().strftime(STRING_FORMAT)
        self.analyze_method = analyze_method
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)
        self.description = description or ""

    def get_all_images(self):
        """ Recupera as imagens das capturas e as formata para serem retornadas ao front-end.
        Se nenhum erro ocorrer, retorna um json com imagens em formato JPG codificadas em bytes na base64.
        """
        if self.encoded_images is None:
            converted_differentiator = ImagePack.convert_to_bytes(self.differentiator_image, compression=100)
            self.captures_images['diferenciador.jpg'] = converted_differentiator
            self.encoded_images = ImagePack.encode_to_b64(self.captures_images.to_bytes())
            self.captures_images = None
        return self.encoded_images

    def get_xlsx_results(self):
        """ Cria e retorna um arquivo xlsx com os resultados da análise. """
        file = ExcelFile(title='Resultados')
        return file.create(self.general_info(), self.average_info(), self.differentiator_info(),
                           self.captures_info(), self.calibration_info())

    def general_info(self):
        """ Reúne e retorna uma lista de listas com títulos e informações gerais da análise. """
        analyzeType = 'Completa' if self.analyze_method == 'complete' else 'Simples'
        title = ['Informações Gerais', '', '', '', '', '']
        headers = ['Data', 'Duração', 'Taxa de capturas', 'Capturas feitas', 'Tipo de análise', 'Descrição']
        content = [self.initial_date, f'{self.total_time} segundos', f'{self.captures_seg} cap./seg.']
        content.extend([f'{len(self.signals)} cap.', analyzeType, f'{self.description or "Não informada"}'])
        return [title, headers, content]

    def average_info(self):
        """ Reúne títulos e os resultados do diferenciador em uma lista de listas. """
        title = ['Valores Médios', '', '', '']
        headers = ['Vermelho', 'Verde', 'Azul', 'Sinal']
        content = [self.colors_average[2], self.colors_average[1], self.colors_average[0], self.signal_average]
        return [title, headers, content]

    def differentiator_info(self):
        """ Reúne títulos e os resultados do diferenciador em uma lista de listas. """
        title = ['Diferenciador', '', '']
        headers = ['Vermelho', 'Verde', 'Azul']
        content = [self.differentiator[2], self.differentiator[1], self.differentiator[0]]
        return [title, headers, content]

    def captures_info(self):
        """ Reúne títulos e os resultados das capturas em uma lista de listas. """
        title = ['Capturas', '', '', '', '', '']
        header = ['Nº Captura', 'Tempo (segundos)', 'Vermelho', 'Verde', 'Azul', 'Sinal']
        information = [title, header]
        for i, value in enumerate(self.captures):
            row = [i + 1, (i + 1) * self.interval, value[2], value[1], value[0], self.signals[i]]
            information.append(row)
        return information

    def calibration_info(self):
        """ Reúne títulos e os resultados referentes ao gráfico de calibração. """
        if len(self.calibration_values) == 0:
            return []
        information = [['Sinal médio de cada ciclo', ''], ['Ciclo', 'Sinal']]
        for index, value in enumerate(self.calibration_values):
            information.append([index + 1, value])
        return information

    def save_new_analyze_date(self, newDate):
        """ Método relacionado ao salvamento do horário da analise.
        Foi necessário adicionar essa funcionalidade pois o horário do rasp. fica atrasado se utilizado
        sem conexão a internet. Assim, a análise utiliza o horário enviado pelo usuário.
        """
        self.initial_date = datetime.strptime(newDate, STRING_FORMAT).strftime(STRING_FORMAT)
