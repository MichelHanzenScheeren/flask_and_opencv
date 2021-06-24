from app.configuration import FRAME_RATE
import time
from threading import Lock, Thread
from app.domain.packs.image_pack import ImagePack


PADRONIZED_WIDTH = 640  # largura padrão usada na webcam
PADRONIZED_HEIGHT = 480  # altura padrão usada na webcam
WIDTH_INDEX = 3
HEIGHT_INDEX = 4


class VideoCapture:
    """ Classe que possui a lógica de obtenção dos frames da webcam da classe VideoCapture pela biblioteca OpenCV.

    Uma Thread é usada para gerenciar as capturas e garantir que sejam feitas mesmo durante a análise. 
    Um Lock também é usado, para garantir que condições de concorrência não ocorram.
    """

    def __init__(self, set_frame):
        self.set_frame = set_frame  # Método usado para salvar o novo frame obtido na classe correspondente.
        self._is_working = True  # Indicar se a Thread deve continuar executando (falso caso a captura falhe)
        self.video_capture = None  # Instância da classe VideoCapture, da biblioteca OpenCV.
        self.lock_video = Lock()  # Garantir que condições de corrida não ocorram (por causa das threads).
        self.thread = None  # Armazena a Thread atual que gerencia a captura dos frames

    def start_video(self, port):
        """ Método que valida e inicializa a Thread e a captura dos frames da webcam.

        A verificação incial garante que a Thread e a webcam só serão iniciadas se outras não estejam em execução.
        """
        if not self.is_working() or not self.is_valid():
            self.start_video_stream(port)
            self.set_working_state(True)
            self.define_resolution()
            self.start_thread()

    def is_valid(self):
        """ Retorna true se video_capture for uma instância de webcam válida (webcam em uso). """
        with self.lock_video:
            return self.video_capture and self.video_capture.isOpened()

    def is_working(self):
        """ Retorna o valor de _is_working, true por padrão caso nenhum erro ocorra ao capturar frames da webcam. """
        with self.lock_video:
            return self._is_working

    def start_video_stream(self, port):
        """ Método que efetivamente cria a instância de VideoCapture da biblioteca OpenCv.

        Recebe um inteiro correspondente a porta que será usada pela webcam (inicialmente a porta 0).
        Nenhum retorno.
        """
        with self.lock_video:
            self.video_capture = ImagePack.new_stream(port)

    def start_thread(self):
        """ Método responsável por iniciar a Thread que fará a captura dos frames da webcam.

        'target' é a função que ele executará assim que iniciar.
        'daemon' true significa que a thread será finalizada automaticamente se o programa principal for finalizado.
        """
        self.thread = Thread(target=self.capture_webcam_image, daemon=True)
        self.thread.start()

    def capture_webcam_image(self):
        """ Executado apenas pela Thread. Captura frames da webcam e os salva na classe correspondenete.

        'FRAME_RATE' e 'previous' garantem que as capturas terão um intervalo >= 0.04 segundos (+/- 25fps: 1seg/0.04).
        Esse controle foi adicionado para evitar excesso de processamento do raspberry.
        Sem ele, o raspberry não estava dando conta das capturas. 
        """
        try:
            previous = 0
            while self.is_working():
                if (time.time() - previous) >= FRAME_RATE:
                    frame = self.capture_frame()
                    self.set_frame(frame)
                    previous = time.time()
        except Exception as erro:
            print(erro)

    def capture_frame(self):
        """ Método chamado pela Thread para capturar o frame. Sempre retorna uma imagem no padrão OpenCV (ndarray).

        Se _is_working for true e a webcam atual é valida, captura um frame. 
        Caso contrário, retorna uma imagem padrão setada para preto.
        """
        if(self.is_working() and self.is_valid()):
            return self._do_capture()
        return ImagePack.black_image()

    def _do_capture(self):
        """ Método que efetivamente faz a captura do frame. Sempre retorna uma imagem no padrão OpenCV (ndarray). """
        with self.lock_video:
            success, frame = self.video_capture.read()
        self.set_working_state(success)
        return frame if success else ImagePack.black_image()

    def define_resolution(self):
        """ Padroniza a resolução da imagem, independente da webcam utilizada. Padrão é de 480X640 (height X width).

        O parâmetro WIDTH_INDEX (3) diz respeito a largura da imagem (width).
        O parâmetro HEIGHT_INDEX (4) diz respeito a altura da imagem (height).
        Está no planejamento permitir o aumento da resolução, mas a webcam do laboratório tinha resolução máxima 480X640.
        """
        with self.lock_video:
            if(self._not_is_padronized_size()):
                self.video_capture.set(WIDTH_INDEX, PADRONIZED_WIDTH)
                self.video_capture.set(HEIGHT_INDEX, PADRONIZED_HEIGHT)
            res = '\n# RESOLUÇÃO'
            print(f'{res}: {self.video_capture.get(WIDTH_INDEX):.0f}X{self.video_capture.get(HEIGHT_INDEX):.0f} #')

    def _not_is_padronized_size(self):
        padronized_width = self.video_capture.get(WIDTH_INDEX) != PADRONIZED_WIDTH
        return padronized_width or self.video_capture.get(HEIGHT_INDEX) != PADRONIZED_HEIGHT

    def set_working_state(self, condition=True):
        with self.lock_video:
            self._is_working = condition

    def video_status(self):
        """ Retorna a resolução da webcam para uso no front-end (tamanho do container que vai exibir as imagens). """
        if not self.is_valid():
            h, w, success = (PADRONIZED_HEIGHT, PADRONIZED_WIDTH, False)
            self.set_working_state(False)
        else:
            h, w = self.get_video_dimensions()
            self.capture_frame()  # Necessário para captura do primeiro frame e verificação do funcionamento
            success = self.is_working()
        return {'style': f'height:{h}px;min-height:{h}px;width:{w}px;min-width:{w}px;', 'success': success}

    def get_video_dimensions(self):
        """ Retorna a resolução da webcam, uma tupla de inteiros na forma (height, width). """
        with self.lock_video:
            return (int(self.video_capture.get(HEIGHT_INDEX)), int(self.video_capture.get(WIDTH_INDEX)))

    def change(self, new_port):
        """ Método que libera o video atual e inicia uma nova webcam a partir da porta recebida por parâmetro. 

        O parâmetro recebido deve ser um inteiro maior ou igual a zero.
        Caso o processo seja um sucesso, retorna a resolução da webcam.
        Caso algo falhe, retorna uma string vazia.
        """
        with self.lock_video:
            to_dispose = self.video_capture
            self.video_capture = ImagePack.new_stream(new_port)
            self._is_working = True
        self.define_resolution()
        to_dispose.release()
        return self.video_status()

    def turn_off(self):
        """ Método encarregado de parar a Thread e liberar a webcam. """
        self.set_working_state(False)
        with self.lock_video:
            if self.video_capture:
                self.video_capture.release()
                self.video_capture = None
        self.thread = None
