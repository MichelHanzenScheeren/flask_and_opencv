from threading import Lock
from app.domain.packs.image_pack import ImagePack


class Rectangle():
    """ Classe responsável por armazenar e gerenciar o retângulo desenhado pelo usuário.

    Esse retângulo representa a área de interesse da imagem, que será recortada da imagem da webcam 
    (ou enviada pelo upload) no momento da análise.
    """

    def __init__(self):
        self.lock_drawing = Lock()  # Lock usado para evitar condições de corridas.
        self.initial_points_of_rectangle()  # inicializa todos os pontos do retângulo para 0.

    def initial_points_of_rectangle(self):
        with self.lock_drawing:
            self.x_initial = 0  # (x_initial, y_initial)_____
            self.y_initial = 0  # |							|
            self.x_final = 0  # |____________________(x_final, y_final)
            self.y_final = 0

    def define_points_of_rectangle(self, x1, y1, x2, y2):
        """ Recebe os 4 pontos do retângulo, valida-os e os salva temporariamente. 

        Os 4 pontos devem ser inteiros e representar um retângulo válido.
        Nenhum retorno.
        """
        with self.lock_drawing:
            if self.is_int(x1, y1, x2, y2) and self.is_valid_points(x1, y1, x2, y2):
                self.x_initial = min(x1, x2)
                self.y_initial = min(y1, y2)
                self.x_final = self.x_initial + abs(x1 - x2)
                self.y_final = self.y_initial + abs(y1 - y2)

    def is_int(self, x1, y1, x2, y2):
        """ Retorna 'true' se todos os pontos forem valores inteiros. Caso contrário, retorna 'false'. """
        return (type(x1) is int) and (type(y1) is int) and (type(x2) is int) and (type(y2) is int)

    def is_valid_points(self, x1, y1, x2, y2):
        """ Retorna 'true' se os pontos pertencerem a um retângulo válido. Caso contrário, retorna 'false'.  

        Para ser considerado válido, todos os potos do retênagulo precisam ser >= 0.
        Os pontos também devem garantir que o retângulo tenha área diferente de zero.
        """
        greater_than_zero = (x1 >= 0) and (y1 >= 0) and (x2 >= 0) and (y2 >= 0)
        has_area = ((x1 - x2) != 0) and ((y1 - y2) != 0)
        return (greater_than_zero and has_area)

    def is_valid_rectangle(self):
        """ Retorna true se pelo menos um ponto 'x' e um 'y' for diferente de 0. Caso contrário, retorna false. """
        with self.lock_drawing:
            return ((self.x_initial != 0 or self.x_final != 0) and (self.y_initial != 0 or self.y_final != 0))

    def draw_rectangle(self, frame):
        """ Método que recupera os pontos do retângulo, valida-os e desenha no frame recebido como parâmetro. 

        Sempre retorna uma imagem no padrão OpenCV (ndarray). 
        A imagem retornada terá um retângulo desenhado caso exista um retângulo válido salvo.
        """
        if self.is_valid_rectangle():
            ImagePack.draw_rectangle(frame, self.initial_xy(), self.final_xy())
        return frame

    def initial_xy(self):
        """ Retorna o primeiro ponto do retângulo na forma de uma tupla (x, y). """
        with self.lock_drawing:
            return (self.x_initial, self.y_initial)

    def final_xy(self):
        """ Retorna o segundo ponto do retângulo na forma de uma tupla (x, y). """
        with self.lock_drawing:
            return (self.x_final, self.y_final)

    def crop_image(self, image):
        """ Verifica se há um retângulo válido e recorta o frame recebido por parâmetro dentro desse retâgulo.

        Sempre retorna uma imagem no padrão OpenCV (ndarray).
        Caso exista um retângulo válido salvo, recorta a imagem dentro dele e a retorna.
        Caso contrário, retorna a própria imagem original.
        """
        if(self.is_valid_rectangle()):
            with self.lock_drawing:
                return image[self.y_initial:self.y_final, self.x_initial:self.x_final]
        return image
