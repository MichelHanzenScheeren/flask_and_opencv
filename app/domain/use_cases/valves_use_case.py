from app.domain.errors.app_error import AppError


class ValvesUseCase():
    def __init__(self, valves_control):
        self.valves_control = valves_control

    def _success_response(self, message='Operação concluída', data=''):
        return {'message': message, 'data': data}, 200

    def error_response(self, error):
        if type(error) is AppError:
            return {'success': False, 'key': error.origin, 'message': str(error)}
        return {'key': 'unkown', 'message': f'Erro desconhecido ({str(error)})'}, 404
