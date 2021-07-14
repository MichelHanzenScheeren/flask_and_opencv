import cv2.cv2 as cv2
import numpy
from pyzip import PyZip
from io import BytesIO
from base64 import b64encode


class ImagePack():
    """ Classe de métodos estáticos que encapsula todas as chamadas diretas a biblioteca OpenCv.

    Foi criada pensando em reduzir os possíveis impactos de uma mudança de biblioteca.
    Também reúne os usos da biblioteca numpy, relacionada com a biblioteca OpenCV.
    Conta ainda com criação de zip (PyZip), de bytes (BytesIO) e de coversão a b64 (b64encode)
    """

    @staticmethod
    def new_stream(port):
        """ Cria e retorna uma intância da classe VideoCapture, própria da biblioteca OpenCV. """
        return cv2.VideoCapture(port)

    @staticmethod
    def is_valid_webcam(test_port):
        """ Verifica se determinada porta recebida por parâmetro corresponde a de uma webcam válida. """
        video = ImagePack.new_stream(test_port)
        is_valid = video is not None and video.isOpened()
        ImagePack.dispose_video_stream(video)
        return is_valid

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
    def compress_and_convert_to_bytes(image):
        encode_param = [cv2.IMWRITE_JPEG_QUALITY, 80]
        return (cv2.imencode('.jpg', image, encode_param)[1]).tobytes()

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
        return isinstance(image, numpy.ndarray)

    @staticmethod
    def encode_to_b64(file):
        return b64encode(file)

    @staticmethod
    def create_zip_file():
        return PyZip()

    @staticmethod
    def create_bytes_file():
        return BytesIO()
