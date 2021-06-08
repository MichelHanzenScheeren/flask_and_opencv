from app.configuration import GROUP_NUMBER, KEY_SEPARATOR, LINE_NUMBER
from app.domain.errors.app_error import AppError
from app.domain.models.programming_line import ProgrammingLine


class ProgrammingGroup():
    def __init__(self):
        self.sequence = -1
        self.lines = []

    def from_dictionary(self, key_name, dictionary):
        self._validate_parameters(key_name, dictionary)
        self.sequence = int(key_name.strip().split(KEY_SEPARATOR)[-1])
        for key in dictionary.keys():
            line = ProgrammingLine().from_dictionary(key, dictionary[key])
            self.lines.append(line)
        return self

    def _validate_parameters(self, key_name, dictionary):
        if type(key_name) is not str:
            message = 'Id de grupo inválido'
            raise AppError('ProgrammingGroup.key_name',  message)
        if type(dictionary) is not dict:
            message = 'Grupo de programação não corresponde a um json válido'
            raise AppError('ProgrammingGroup.dictionary',  message)

    def _validate(self):
        message = ''
        if type(self.sequence) is not int or self.sequence == -1:
            message = f'Valor inválido para parâmetro {GROUP_NUMBER}'
        elif type(self.lines) is not list:
            message = f'Valor de "{LINE_NUMBER}" inválido para {GROUP_NUMBER}'
        if not message == '':
            raise AppError('ProgrammingGroup', message)
