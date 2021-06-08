from app.configuration import *
from app.domain.errors.app_error import AppError


class ProgrammingLine():
    def __init__(self):
        self.line_number = -1
        self.cycle_start = False
        self.sleep_time = 0
        self.open_valves = []

    def from_dictionary(self, key_name, dictionary):
        self._validate_parameters(key_name, dictionary)
        self.line_number = int(key_name.strip().split(KEY_SEPARATOR)[-1])
        self.cycle_start = dictionary[CYCLE_START]
        self.sleep_time = dictionary[SLEEP_TIME]
        self.open_valves = dictionary[OPEN_VALVES]
        self._validate()
        return self

    def _validate_parameters(self, key_name, dictionary):
        if type(key_name) is not str:
            message = 'Id da linha inválido'
            raise AppError('ProgrammingLine.key_name',  message)
        if type(dictionary) is not dict:
            message = 'Linha de programação não corresponde a um json válido'
            raise AppError('ProgrammingLine.dictionary',  message)

    def _validate(self):
        message = ''
        if type(self.line_number) is not int or self.line_number == -1:
            message = f'Valor inválido para parâmetro "{LINE_NUMBER}"'
        elif type(self.cycle_start) is not bool:
            message = f'Valor inválido para parâmetro "{CYCLE_START}"'
        elif not (type(self.sleep_time) is int or type(self.sleep_time) is float):
            message = f'Valor inválido para parâmetro "{SLEEP_TIME}"'
        elif type(self.open_valves) is not list:
            message = f'Valor inválido para parâmetro "{OPEN_VALVES}"'
        if not message == '':
            raise AppError('ProgrammingLine.line_number', message)
