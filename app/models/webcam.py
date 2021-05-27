from app.models.rectangle import Rectangle
from app.models.video_capture import VideoCapture
from app.models.image_pack import ImagePack
from app.models.frame import Frame
import time


class Webcam():
    """ Classe responsável por todo o controle relacionado ao uso da webcam.

    A classe gerencia a instância opencv do VideoCapture, além de fazer as capturas dos frames da webcam.
    Também armazena e manipula o frame captado e gerencia a porta atual.
    Por fim, armazena e manipula a imagem enviada opcionalmente pelo usuário.
    """

    def __init__(self):
        # Variável global que armazena a porta atualmente usada pela webcam (inicia como porta 0).
        self.current_port = 0
        # Variável global que armazena a porta atualmente usada pela webcam (inicia como porta 0).
        self.rectangle = Rectangle()
        # Variável global que armazena o frame enviado pelo usuário (opcional - para o diferenciador).
        self.uploaded_frame = Frame()
        # Variável global que armazena o último frame capturado pela webcam.
        self.captured_frame = Frame()
        # Encapsula a manipulação direta da instância OpenCV do VideoCapture.
        self.video_capture = VideoCapture(self.captured_frame.set_frame)

    def init_webcam(self):
        """ Método que inicia as capturas da webcam. Nenhum retorno. """
        self.video_capture.start_video(self.current_port)

    def video_status_and_port(self):
        """ Obtêm e retorna as informações principais relacionadas ao frame capturado na webcam.  

        Retorna altura e largura do frame (por padrão 480X640) e a porta atual.
        O retorno está no formato json. 
        """
        status = self.video_capture.video_status()
        status['current'] = self.current_port
        return status

    def webcans_list(self):
        """ retorna a lista de webcans disponíveis atualmente. 

        O método tenta abrir as portas de webcam diferentes da atual e finaliza quando falha pela primeira vez.
        Isso se baseia no princípio de que as portas da webcam sempre iniciam no 0 (principal do computador) e vão aumentando de 1 em 1.
        """
        list_webcans = []
        for index in range(100):
            if index == self.current_port:
                continue
            if not ImagePack.is_valid_webcam(index):
                break
            list_webcans.append(index)
        list_webcans.insert(self.current_port, self.current_port)
        return list_webcans

    def change_current_webcam(self, index):
        """ Método responsável por alterar a webcam usada no sistema. 

        Recebe um inteiro correspondente a nova porta webcam que será usada.
        Retorna string vazia em caso de falha. 
        Retorna as dimensões do frame da nova webcam em caso de sucesso. 
        """
        if self.is_invalid_index(index):
            return ''
        self.current_port = index
        return self.video_capture.change(index)

    def is_invalid_index(self, index):
        return index is None or (type(index) is not int) or index < 0

    def stream_webcam(self):
        """ Método que obtêm o frame atual e o retorna particionado em forma de bits.

        O frame atual pode ser o de um upload ou o obtido da webcam.
        O retorno particionado é graças ao yield (tipo de retorno especial do python3). 
        A imagem é retornada em bits e no formato jpeg.
        Variáveis 'FRAME_RATE' e 'previous' garantem que a resposta terá um intervalo >= 0.04 segundos (+/- 25fps) 
        """
        try:
            FRAME_RATE, previous = 0.04, 0
            while True:
                if (time.time() - previous) >= FRAME_RATE:
                    img = self.get_image()
                    yield(b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n\r\n')
                    previous = time.time()
        except Exception as exception:
            print(exception)

    def get_image(self):
        """ Retorna a imagem atualmente em foco do projeto.

        A imagem pode ser tanto a de um upload feito pelo usuário ou o frame atual da webcam.
        A imagem retornada está no formato jpeg e contêm o retângulo desenhado pelo usuário (caso exista).
        """
        try:
            if(self.uploaded_frame.is_valid()):
                copy = self.uploaded_frame.get_copy()
            else:
                copy = self.captured_frame.get_copy()
            return self.draw_and_convert_frame(copy)
        except:
            return ImagePack.encode_to_jpg(ImagePack.black_image())

    def draw_and_convert_frame(self, copy):
        drawed_image = self.rectangle.draw_rectangle(copy)
        return ImagePack.encode_to_jpg(drawed_image)

    def get_differentiator_image(self):
        """ Obtém e retorna a imagem que será usada como diferenciador na classe Analyze.

        A imagem pode ser tanto a de um upload do usuário quanto a do frame atual da webcam.
        A imagem é recortada caso um retângulo tenha sido desenhado pelo usuário (área de interesse da imagem).
        A imagem retornada está no formato padrão do OpenCV (ndarray).
        """
        if(self.uploaded_frame.is_valid()):
            return self.crop_uploaded_image()
        return self.get_cropped_image()

    def crop_uploaded_image(self):
        """ Obtêm e retorna a imagem enviada pelo usuário. 

        A imagem é recortada caso um retângulo tenha sido desenhado pelo usuário (área de interesse da imagem).
        A imagem retornada está no formato padrão do OpenCV (ndarray).
        """
        copy = self.uploaded_frame.get_copy()
        self.uploaded_frame.clear()
        return self.rectangle.crop_image(copy)

    def get_cropped_image(self):
        """ Obtêm e retorna o último frame capturado pela webcam. 

        A imagem é recortada caso um retângulo tenha sido desenhado pelo usuário (área de interesse da imagem).
        A imagem retornada está no formato padrão do OpenCV (ndarray).
        """
        copy = self.captured_frame.get_copy()
        return self.rectangle.crop_image(copy)

    def save_uploaded_image(self, image):
        """ Recebe uma imagem enviada pelo usuário e armazena para uso posterior.

        A imagem é convertida para o padrão do OpenCV (ndarray).
        Antes de ser salva, a imagem é também redimensionada para o mesmo tamanho do frame atual da webcam.
        Nenhum retorno.
        """
        try:
            frame = ImagePack.convert_to_frame(image)
            video_dimensions = self.video_capture.get_video_dimensions()
            new_image = ImagePack.resize_image(frame, video_dimensions)
            self.uploaded_frame.set_frame(new_image)
        except:
            pass

    def clear_rectangle_and_uploaded_image(self):
        """ Responsável por apagar o retângulo previamente desenhado e apagar a imagem enviada pelo usuário. """
        self.rectangle.initial_points_of_rectangle()
        self.uploaded_frame.clear()

    def clear(self):
        """ Responsável por desativar a captura da webcam e limpar variáveis (como o retângulo a imagem do upload). """
        self.video_capture.turn_off()
        self.clear_rectangle_and_uploaded_image()

    def __del__(self):
        self.video_capture.turn_off()
        self.clear_rectangle_and_uploaded_image()
