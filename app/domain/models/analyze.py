from gc import collect
from time import sleep
from datetime import datetime
from timeit import default_timer
from math import sqrt, pow
from threading import Thread
from app.domain.errors.app_error import AppError
from app.domain.models.results import Results
from app.domain.packs.image_pack import ImagePack


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
        """ Inicia a análise, onde serão salvas as capturas de acordo com os parâmetros recebidos.

        'analize_method' é uma string que indica o método de análise (simple ou complete)
        'total_time' é um valor inteiro > 0 que corresponde ao tempo total da análise (em segundos).
        'captures_seg' é um inteiro 0 < X < 10 que indica quantas capturas serão feitas a cada segundo de análise.
        'description' é uma string opcional para descrever a análise, exibida nos resultados e salva no xlsx gerado.
        'get_cropped_image' é um método da Webcam que retorna o frame atual recortado e em formato ndarray.
        'programming_interpret' é um método que cuida da interpretação do arquivo de programação das válvulas.
        """
        analize_method,  total_time, captures_seg = form['analizeMethod'], form['time'], form['qtd']
        description, select_date, user_date = form['description'], form['selectDate'], form['userDate']
        self.validate_form(analize_method, total_time, captures_seg)
        self.results.initialize(analize_method, int(total_time), int(captures_seg), description, select_date, user_date)
        self._start(get_cropped_image, programming_interpret)

    def validate_form(self, analize_method, time, captures):
        """ Verifica se os valores recebidos são válidos para a análise. """
        if len(self.results.captures) != 0 or len(self.results.differentiator) == 0:
            raise AppError('Analyze.validade', 'É preciso capturar o difenenciador antes de dar início a análise')
        if not (analize_method == 'simple' or analize_method == 'complete'):
            raise AppError('Analyze.validade', 'O método de análise informado não é válido')
        if not time.isdigit() or (analize_method == 'simple' and int(time) < 1):
            raise AppError('Analyze.validade', 'O tempo de análise informado não é válido')
        if not captures.isdigit() or int(captures) < 1 or int(captures) > 10:
            raise AppError('Analyze.validade', 'O número de capturas informado não é válido')

    def _start(self, get_cropped_image, programming_interpret):
        """ Método que encaminha a análise para as respectivas funções de acordo com seu tipo (simple ou complete) """
        if self.results.analize_method == 'simple':
            self.do_simple_analyze(get_cropped_image)
            self.calculate_signal()
        else:
            cycles_informations = []
            thread = self.start_valves_thread(programming_interpret, cycles_informations)
            self.do_complete_analyze(get_cropped_image, thread)
            self.calculate_signal()
            self.calculate_calibrate_points(cycles_informations)

    def do_simple_analyze(self, get_cropped_image):
        """" Método que salva os frames e calcula a média de cores correspondentes a captura na análise simples.

        "to_discount" e a lógica envolvida garantem que as conversões e cálculos não vão interferir significativamente
        no interalo de capturas, descontando esse tempo do sleep.
        O sleep garante que a relação tempo total e intervalo entre capturas seja seguido.
        """
        repetitions = int(self.results.total_time * self.results.captures_seg)
        for _ in range(0, repetitions):
            image = get_cropped_image()
            to_discount = default_timer()
            self.save_image_color_average(image)
            self.save_converted_image(image)
            discounted_interval = self.results.interval - (default_timer() - to_discount)
            if discounted_interval > 0:
                sleep(discounted_interval)

    def save_image_color_average(self, image):
        """" Método que efetivamente salva a média de cores da captura atual na lista de capturas. """
        average = self.calculate_average(image)
        self.results.captures.append(average)

    def save_converted_image(self, image):
        """" Comprime e converte a imagem para mantê-la em memória.

        Foi necessário implementar a compactação e conversão durante a análise para poupar memória RAM.
        Caso contrário, a capacidade de fazer análises grandes seria comprometida (faltava memória de trabalho).
        """
        converted = ImagePack.compress_and_convert_to_bytes(image)
        index = len(self.results.captures_images) + 1
        self.results.captures_images[f'captura_{index}.jpg'] = converted

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
        """ Método que inicia a thread que cuida da abertura e fechamento das válvulas na análise completa.

        A thread é retornada para que seu fim seja controlado (ela define o fim das capturas da webcam).
        """
        thread = Thread(target=programming_interpret, args=(cycles_informations,))
        thread.start()
        return thread

    def do_complete_analyze(self, get_cropped_image, thread):
        """" Método que salva os frames e calcula a média de cores das captura na análise completa.

        "to_discount" e a lógica envolvida garantem que as conversões e cálculos não vão interferir significativamente
        no interalo de capturas, descontando esse tempo do sleep.
        O sleep garante que a relação tempo total e intervalo entre capturas seja seguido.
        O fim da análise é definido pelo final da thread que gerencia a abertura e fechamento das válvulas.
        """
        start = datetime.now()
        while(thread.is_alive()):
            image = get_cropped_image()
            self.results.captures_times.append(datetime.now())
            to_discount = default_timer()
            self.save_image_color_average(image)
            self.save_converted_image(image)
            discounted_interval = self.results.interval - (default_timer() - to_discount)
            if(discounted_interval > 0):
                sleep(discounted_interval)
        self.results.total_time = (datetime.now() - start).seconds

    def calculate_calibrate_points(self, cycles_informations):
        """" Método que gera os pontos para o gráfico de calibração.

        "cycles_information" é uma lista com informações de início e fim dos ciclo de abertura das válvulas.
        Essas informações são usadas para filtrar quais capturas pertencem a cada ciclo.
        Cada ciclo possui uma lista interna com mais 3 dados (ciclos de 3 iterações - análise em triplicata).
        De cada uma das 3 repetições, pega-se o maior sinal.
        A média do maior sinal de cada repetição gera uma nova coordenada do gráfico (coordenada x).
        """
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
        """ Liberação da memória de análise anterior.

        O "del" e o "collect" são usados para garantir explicitamente que os recursos serão liberados,
        já qe o rasp não os possui em abundância.
        """
        del self.results
        collect()  # forçar explicitamente a coleta de memória pelo garbage collector do python
        self.results = Results()
