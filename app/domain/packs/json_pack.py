import json
from app.domain.errors.app_error import AppError


class JsonPack():
    """ Classe de métodos estáticos encarregada da leitura e escrita de arquivos json. """

    @staticmethod
    def read(path):
        try:
            with open(path) as json_file:
                return json.load(json_file)
        except:
            message = 'Não foi possível ler o json informado'
            assert AppError('JsonPack.read', message)

    @staticmethod
    def write(path, data):
        try:
            with open(path, 'w+') as json_file:
                json.dump(data, json_file, indent=4, sort_keys=True)
        except:
            message = 'Não foi possível escrever no caminho informado'
            assert AppError('JsonPack.read', message)
