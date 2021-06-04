from datetime import datetime
from app.domain.errors.app_error import AppError
from app.configuration import SAVED_DATE, JSON_PROGRAMMING_PATH, STRING_FORMAT
from app.domain.packs.json_pack import JsonPack


class SaveJsonProgramming():
    def __init__(self, dictionary):
        self._dictionary = dictionary
        self._validate_dictionary()

    def _validate_dictionary(self):
        if type(self._dictionary) is not dict:
            message = 'Dados inváldos para criação do arquivo json'
            raise AppError('CreateJsonProgramming.dictionary', message)

    def create(self):
        self._dictionary[SAVED_DATE] = datetime.now().strftime(STRING_FORMAT)
        JsonPack.write(JSON_PROGRAMMING_PATH, self._dictionary)
