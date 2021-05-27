from time import sleep
from math import sqrt, pow
from app.models.results import Results


class Analyze():
    """ Clase que encapsula todos os processos de análise das capturas.

    Aqui que são obtidas as médias das cores do diferenciador e capturas.
    Também é feito o calculo dos sinais a partir dos resultados anteriores.
    Os resultados em si são salvos na classe Results.
    """

    def __init__(self):
        self.results = Results()

    def calculate_differentiator(self, get_differentiator_image):
        """ Método que Calcula a média BGR (padrão OpenCV) dos pixels do diferenciador.

        Se tudo correr bem, retorna os resultados obtidos como uma lista [R, G, B].
        Se algum erro ocorrer, retorna uma string vazia.
        """
        try:
            return self._calculate_differentiator(get_differentiator_image)
        except Exception as exception:
            print(exception)
            return ''

    def _calculate_differentiator(self, get_differentiator_image):
        """ Método que efetivamente salva a imagem do diferenciador e calcula sua média de cores dos pixels.

        'get_differentiator_image' é um método da classe Webcam que retorna uma imagem padrão OpenCV (ndarray)
        A imagem do diferenciador pode tanto ser fruto de um upload do usuário quanto o frame atual capturado no diferenciador.
        Os resultados são salvos como uma lista BGR ([B, G, R]) e retornados como uma lista [R, G, B].
        """
        image = get_differentiator_image()
        self.results.differentiator_image = image
        result = self.calculate_average(image)
        self.results.differentiator = result
        return f'[{result[2]:.3f}, {result[1]:.3f}, {result[0]:.3f}]'

    def calculate_average(self, image):
        """ Calcula a média de cores de um frame recebido como parâmetro. Retorna uma lista no padrão [B, G, R]. """
        return image.mean(axis=0).mean(axis=0)

    def start_analyze(self, total_time, captures_seg, description, select_date, user_date, get_cropped_image):
        """ Inicia a análise propriamente dita, onde serão salvas as capturas de acordo com os parâmetros recebidos.

        'total_time' é um valor inteiro > 0 que corresponde ao tempo total da análise (em segundos).
        'captures_seg' é um inteiro 0 < X < 10 que indica quantas capturas devem ser feitas a cada segundo de análise.
        'description' é uma string opcional que descreve o análise, exibida na página de resultados e salva no xlsx gerado.
        'get_cropped_image' é um método da classe Webcam que retorna o frame atual da webcam recortado e em formato ndarray.
        """
        if (self.form_is_valid(total_time, captures_seg)):
            self.results.initialize(int(total_time), int(captures_seg), description, select_date, user_date)
            self.save_analyze_frames(get_cropped_image)
            self.do_analyze()
            self.calculate_signal()
        else:
            raise Exception('Formulário inválido!')

    def form_is_valid(self, time, captures):
        """ Verifica se os valores recebidos são válidos para a análise. """
        is_digit = time.isdigit() and captures.isdigit()
        valid_range = int(time) >= 1 and int(captures) >= 1 and int(captures) <= 10
        return is_digit and valid_range

    def save_analyze_frames(self, get_cropped_image):
        """" Método que salva os frames correspondentes a captura.

        O sleep garante que a relação tempo total e intervalo entre capturas seja seguido.
        Nenhum retorno.
        """
        repetitions = int(self.results.total_time * self.results.captures_seg)
        for _ in range(0, repetitions):
            image = get_cropped_image()
            self.results.captures_images.append(image)
            sleep(self.results.interval)

    def do_analyze(self):
        """ Método em que são calculadas as médias de cores de cada captura salva. """
        for image in self.results.captures_images:
            average = self.calculate_average(image)
            self.results.captures.append(average)

    def calculate_signal(self):
        """ Método em que os sinais são calculados. 

        Um 'sinal' é a distância vetorial entre a média de cores de uma captura e a média de cores do diferenciador.
        """
        differentiator = self.results.differentiator
        for capture in self.results.captures:
            signal = sqrt(
                pow(capture[0] - differentiator[0], 2) +
                pow(capture[1] - differentiator[1], 2) +
                pow(capture[2] - differentiator[2], 2)
            )
            self.results.signals.append(signal)

    def clear(self):
        if len(self.results.differentiator) != 0:
            self.results = Results()
