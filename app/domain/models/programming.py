from datetime import datetime
from app.configuration import *
from app.domain.errors.app_error import AppError
from app.domain.models.programming_group import ProgrammingGroup


class Programming():
    def __init__(self):
        self.valves_quantity = 0
        self.triplicate = False
        self.subtitle = {}
        self.valves_program = []

    def from_dictionary(self, dictionary):
        self._validate_parameter(dictionary)
        self.valves_quantity = dictionary[VALVES_QUANTITY]
        self.triplicate = dictionary[WORKING_IN_TRIPLICATE]
        self.subtitle.clear()
        for key in dictionary[SUBTITLE].keys():
            self.subtitle[key] = dictionary[SUBTITLE][key]
        self.valves_program.clear()
        for key in dictionary[PROGRAMMING]:
            json_group = dictionary[PROGRAMMING][key]
            group = ProgrammingGroup().from_dictionary(key, json_group)
            self.valves_program.append(group)
        self._validate()
        return self

    def _validate_parameter(self, dictionary):
        if type(dictionary) is not dict:
            message = 'O arquivo não corresponde a um json de programação válido'
            raise AppError('Programming.dictionary',  message)

    def _validate(self):
        message = f''
        if type(self.valves_quantity) is not int:
            message = f'Valor inválido para parâmetro "{VALVES_QUANTITY}"'
        elif type(self.triplicate) is not bool:
            message = f'Valor inválido para parâmetro "{WORKING_IN_TRIPLICATE}"'
        elif type(self.subtitle) is not dict:
            message = f'Valor inválido para parâmetro "{SUBTITLE}"'
        elif type(self.valves_program) is not list:
            message = f'Valor inválido para parâmetro "{PROGRAMMING}"'
        if not message == '':
            raise AppError('Programming', message)
