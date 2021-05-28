import cv2.cv2 as cv2
import numpy


class ImagePack():
    """ Classe de métodos estáticos que encapsula todas as chamadas diretas a biblioteca OpenCv.

    Foi criada pensando em reduzir os possíveis impactos de uma mudança de biblioteca.
    Também reúne os usos da biblioteca numpy, relacionada com a biblioteca OpenCV.
    """

    @staticmethod
    def new_stream(port):
        """ Cria e retorna uma intância da classe VideoCapture, própria da biblioteca OpenCV. """
        return cv2.VideoCapture(port)

    @staticmethod
    def is_invalid_webcam(test_port):
        """ Verifica se determinada porta recebida por parâmetro corresponde a de uma webcam válida. """
        video = ImagePack.new_stream(test_port)
        is_invalid = video is None or not video.isOpened()
        ImagePack.dispose_video_stream(video)
        return is_invalid

    @staticmethod
    def dispose_video_stream(video):
        if video is not None:
            video.release()

    @staticmethod
    def draw_rectangle(frame, initial_xy, final_xy):
        """ Desenha as bordas vermelhas de um reângulo iniciado em  'initial_xy' e finalizado em 'final_xy'. 

        'initial_xy' e 'final_xy' são tuplas da forma (x, y).
        Nenhum valor é retornado.
        """
        red_color = (0, 0, 255)  # formato bgr (no lugar de rgb)
        cv2.rectangle(frame, initial_xy, final_xy, red_color, thickness=1)

    @staticmethod
    def convert_to_bytes(image):
        return ImagePack.encode_to_jpg(image).tobytes()

    @staticmethod
    def encode_to_jpg(image):
        return cv2.imencode('.jpg', image)[1]

    @staticmethod
    def convert_to_frame(image):
        """ Converte uma imagem comum (normalmente jpg) em uma imagem OpenCV (ndarray). """
        numpy_img = numpy.fromstring(image.read(), numpy.uint8)
        cv2_image = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
        return cv2_image

    @staticmethod
    def resize_image(image, dimensions):
        """ Redimensiona frame OpenCV (ndarray) para as dimensões recebidas em forma de tupla (height, width). """
        h, w = dimensions
        return cv2.resize(image, (w, h))

    @staticmethod
    def black_image():
        """ Retorna um ndarray (imagem OpenCV) com todos os bits setados em 0 (cor preta) no tamanho 480X640. """
        return numpy.zeros((480, 640, 3), numpy.uint8)

    @staticmethod
    def validate_image(image):
        """ Verifica se uma imagem qualquer é uma imagem OpenCV válida (instância de ndaray). """
        return isinstance(image, numpy.ndarray)
