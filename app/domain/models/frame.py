from threading import Lock
from app.domain.packs.image_pack import ImagePack


class Frame:
    """ Classe que encapsula o armazenamento, get/setters e validações de um frame.

    Também possui um lock para evitar possíveis condições de corrida.
    """

    def __init__(self):
        self._frame = None  # armazena o frame.
        self._lock = Lock()  # Lock do frame para garantir que condições de corrida não ocorram.

    def set_frame(self, new_frame):
        with self._lock:
            self._frame = new_frame

    def get_copy(self):
        """ Cria uma cópia do frame atual para ser retornada a aplicação.

        Uma cópia é criada para garantir que o retângulo que será desenhado não interfira na análise.
        Se nenhum frame estiver salvo, retorna None.
        Caso um frame exista, retorna-o no padrão OpenCV (ndarray).
        """
        with self._lock:
            if self._frame is None:
                return None
            return self._frame.copy()

    def is_valid(self):
        with self._lock:
            return ImagePack.validate_image(self._frame)

    def clear(self):
        with self._lock:
            self._frame = None
