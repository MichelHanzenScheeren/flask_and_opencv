from app.configuration import KEY_SEPARATOR
from app.domain.errors.app_error import AppError
from app.domain.models.programming_line import ProgrammingLine


class ProgrammingGroup():
    def __init__(self):
        self.lines = []

    def from_dictionary(self, key_name, dictionary):
        self._validate_parameters(key_name, dictionary)
        self.sequence = int(key_name.strip().split(KEY_SEPARATOR)[-1])
        for key in dictionary.keys():
            line = ProgrammingLine().from_dictionary(key, dictionary.get(key))
            self.lines.append(line)
        self._validate()
        return self

    def _validate_parameters(self, key_name, dictionary):
        if type(key_name) is not str or len(key_name) == 0 or not key_name[-1].isdigit():
            message = 'Id de grupo inválido'
            raise AppError('ProgrammingGroup.key_name', message)
        if type(dictionary) is not dict:
            message = 'Grupo de programação não corresponde a um json válido'
            raise AppError('ProgrammingGroup.dictionary', message)

    def _validate(self):
        message = ''
        if type(self.sequence) is not int or self.sequence < 0:
            message = 'Valor inválido para parâmetro "id_grupo"'
        elif type(self.lines) is not list or len(self.lines) == 0:
            message = 'Valor inválido para parâmetro "linha"'
        if message != '':
            raise AppError('ProgrammingGroup', message)
