from datetime import datetime
from app.configuration import VALVES_QUANTITY, WORKING_IN_TRIPLICATE, SUBTITLE, PROGRAMMING
from app.domain.errors.app_error import AppError
from app.domain.models.programming_group import ProgrammingGroup


class Programming():
    def __init__(self):
        self.subtitle = {}
        self.valves_program = []

    def from_dictionary(self, dictionary):
        self._validate_parameter(dictionary)
        self.valves_quantity = dictionary.get(VALVES_QUANTITY)
        self.triplicate = dictionary.get(WORKING_IN_TRIPLICATE)
        self.subtitle.clear()
        for key in (dictionary.get(SUBTITLE) or {}).keys():
            self.subtitle[key] = dictionary[SUBTITLE][key]
        self.valves_program.clear()
        for key in dictionary.get(PROGRAMMING) or []:
            json_group = dictionary[PROGRAMMING][key]
            group = ProgrammingGroup().from_dictionary(key, json_group)
            self.valves_program.append(group)
        self._validate()
        return self

    def _validate_parameter(self, dictionary):
        if type(dictionary) is not dict:
            message = 'O arquivo não corresponde a um json de programação válido'
            raise AppError('Programming.dictionary', message)

    def _validate(self):
        message = ''
        if type(self.valves_quantity) is not int:
            message = f'Valor inválido para parâmetro "{VALVES_QUANTITY}"'
        elif type(self.triplicate) is not bool:
            message = f'Valor inválido para parâmetro "{WORKING_IN_TRIPLICATE}"'
        elif type(self.subtitle) is not dict:
            message = f'Valor inválido para parâmetro "{SUBTITLE}"'
        elif type(self.valves_program) is not list or len(self.valves_program) == 0:
            message = f'Valor inválido para parâmetro "{PROGRAMMING}"'
        if message != '':
            raise AppError('Programming', message)
