from time import sleep
from math import sqrt, pow
from datetime import datetime
from threading import Thread
from app.domain.errors.app_error import AppError
from app.domain.models.results import Results


class Analyze():
    """ Clase que encapsula todos os processos de análise das capturas.

    Aqui que são obtidas as médias das cores do diferenciador e capturas.
    Também é feito o calculo dos sinais a partir dos resultados anteriores.
    Os resultados em si são salvos na classe Results.
    """

    def __init__(self):
        self.results = Results()

    def calculate_differentiator(self, differentiator_image):
        """ Método que Calcula a média BGR (padrão OpenCV) dos pixels do diferenciador.

        'differentiator_image' é uma imagem padrão OpenCV (ndarray)
        A imagem do diferenciador pode tanto ser fruto de um upload do usuário quanto o frame atual capturado no diferenciador.
        Os resultados são salvos como uma lista BGR ([B, G, R]) e retornados como uma lista [R, G, B].
        """
        self.results.differentiator_image = differentiator_image
        result = self.calculate_average(differentiator_image)
        self.results.differentiator = result
        return [f'{result[2]:.3f}', f'{result[1]:.3f}', f'{result[0]:.3f}']

    def calculate_average(self, image):
        """ Calcula a média de cores de um frame recebido como parâmetro. Retorna uma lista no padrão [B, G, R]. """
        return image.mean(axis=0).mean(axis=0)

    def start_analyze(self, form, get_cropped_image, programming_interpret):
        """ Inicia a análise propriamente dita, onde serão salvas as capturas de acordo com os parâmetros recebidos.

        'analizeMethod' é uma string que indica o método de análise (simple ou complete)
        'total_time' é um valor inteiro > 0 que corresponde ao tempo total da análise (em segundos).
        'captures_seg' é um inteiro 0 < X < 10 que indica quantas capturas devem ser feitas a cada segundo de análise.
        'description' é uma string opcional para descreevr a análise, exibida nos resultados e salva no xlsx gerado.
        'get_cropped_image' é um método da Webcam que retorna o frame atual recortado e em formato ndarray.
        'programming_interpret' cuida da interpretação do arquivo de programação das válvulas.
        """
        analizeMethod, total_time, captures_seg,  = form['analizeMethod'], form['time'], form['qtd'],
        description, select_date, user_date = form['description'], form['selectDate'], form['userDate']
        self.validate_form(analizeMethod, total_time, captures_seg)
        self.results.initialize(analizeMethod, int(total_time), int(captures_seg), description, select_date, user_date)
        self._start(get_cropped_image, programming_interpret)

    def _start(self, get_cropped_image, programming_interpret):
        if self.results.analizeMethod == 'simple':
            self.simple_save_analyze_frames(get_cropped_image)
            self.do_analyze()
            self.calculate_signal()
        else:
            cycles_informations = []
            thread = self.start_valves_thread(programming_interpret, cycles_informations)
            self.complete_save_analyze_frames(get_cropped_image, thread)
            self.do_analyze()
            self.calculate_signal()
            self.calculate_calibrate_points(cycles_informations)

    def validate_form(self, analizeMethod, time, captures):
        """ Verifica se os valores recebidos são válidos para a análise. """
        if not (analizeMethod == 'simple' or analizeMethod == 'complete'):
            raise AppError('O método de análise informado não é válido')
        if not time.isdigit() or (analizeMethod == 'simple' and int(time) < 1):
            raise AppError('O tempo de análise informado não é válido')
        if not captures.isdigit() or int(captures) < 1 or int(captures) > 10:
            raise AppError('O número de capturas informado não é válido')

    def simple_save_analyze_frames(self, get_cropped_image):
        """" Método que salva os frames correspondentes a captura.

        O sleep garante que a relação tempo total e intervalo entre capturas seja seguido.
        Nenhum retorno.
        """
        repetitions = int(self.results.total_time * self.results.captures_seg)
        for _ in range(0, repetitions):
            image = get_cropped_image()
            self.results.captures_times.append(datetime.now())
            self.results.captures_images.append(image)
            sleep(self.results.interval)

    def do_analyze(self):
        """ Método em que são calculadas as médias de cores de cada captura salva. """
        for image in self.results.captures_images:
            average = self.calculate_average(image)
            self.results.captures.append(average)

    def calculate_signal(self):
        """ 'Sinal' é a distância vetorial da média de cores de uma captura e a média de cores do diferenciador. """
        differentiator = self.results.differentiator
        for capture in self.results.captures:
            signal = sqrt(
                pow(capture[0] - differentiator[0], 2) +
                pow(capture[1] - differentiator[1], 2) +
                pow(capture[2] - differentiator[2], 2)
            )
            self.results.signals.append(signal)

    def start_valves_thread(self, programming_interpret, cycles_informations):
        thread = Thread(target=programming_interpret, args=(cycles_informations,))
        thread.start()
        return thread

    def complete_save_analyze_frames(self, get_cropped_image, thread):
        start = datetime.now()
        while(thread.is_alive()):
            image = get_cropped_image()
            self.results.captures_times.append(datetime.now())
            self.results.captures_images.append(image)
            print('*** PRINCIPAL Imagem salva!')
            sleep(self.results.interval)
        print('*** PRINCIPAL FIM')
        self.results.total_time = (datetime.now() - start).seconds

    def calculate_calibrate_points(self, cycles_informations):
        times = self.results.captures_times
        for group in cycles_informations:
            biggers_signals = []
            for cycle in group.information:
                signals_index = [i for i, x in enumerate(times) if x > cycle.start and x <= cycle.end]
                bigger_signal_index = max(signals_index, key=lambda item: self.results.signals[item])
                biggers_signals.append(self.results.signals[bigger_signal_index])
            average_signal = sum(biggers_signals) / float(len(biggers_signals))
            self.results.calibration_values.append(average_signal)

    def clear(self):
        if len(self.results.differentiator) != 0:
            self.results = Results()
