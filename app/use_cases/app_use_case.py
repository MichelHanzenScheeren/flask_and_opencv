from app.errors.app_error import AppError
from app.models.webcam import Webcam
from app.models.analyze import Analyze


class AppUseCase():
    def __init__(self, non_recoverable_error):
        self.webcam = Webcam()
        self.analyze = Analyze()
        self._non_recoverable_error = non_recoverable_error

    def _success_response(self, message='Operação concluída', data=''):
        return {'success': True, 'message': message, 'data': data}

    def _error_response(self, error):
        if type(error) is AppError:
            return {'success': False, 'key': error.origin, 'message': str(error)}
        return {'success': False, 'key': 'unkown', 'message': f'Erro desconhecido ({str(error)})'}

    def _non_recoverable_error_response(self):
        return self._non_recoverable_error()
