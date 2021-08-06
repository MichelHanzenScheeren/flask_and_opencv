from app.configuration import KEY_SEPARATOR, CYCLE_START, SLEEP_TIME, OPEN_VALVES
from app.domain.errors.app_error import AppError


class ProgrammingLine():
    def __init__(self):
        self.open_valves = []

    def from_dictionary(self, key_name, dictionary):
        self._validate_parameters(key_name, dictionary)
        self.line_number = int(key_name.strip().split(KEY_SEPARATOR)[-1])
        self.cycle_start = dictionary.get(CYCLE_START)
        self.sleep_time = dictionary.get(SLEEP_TIME)
        self.open_valves = dictionary.get(OPEN_VALVES)
        self._validate()
        return self

    def _validate_parameters(self, key_name, dictionary):
        if type(key_name) is not str or len(key_name) == 0 or not key_name[-1].isdigit():
            message = 'Id da linha inválido'
            raise AppError('ProgrammingLine.key_name', message)
        if type(dictionary) is not dict:
            message = 'Linha de programação não corresponde a um json válido'
            raise AppError('ProgrammingLine.dictionary', message)

    def _validate(self):
        message = ''
        if type(self.line_number) is not int or self.line_number == -1:
            message = f'Valor inválido para parâmetro "id_grupo"'
        elif type(self.cycle_start) is not bool:
            message = f'Valor inválido para parâmetro "{CYCLE_START}"'
        elif type(self.sleep_time) is not int or int(self.sleep_time) <= 0:
            message = f'Valor inválido para parâmetro "{SLEEP_TIME}"'
        elif type(self.open_valves) is not list:
            message = f'Valor inválido para parâmetro "{OPEN_VALVES}"'
        if not message == '':
            raise AppError('ProgrammingLine', message)
