from app.domain.errors.app_error import AppError


class ValvesUseCase():
    def __init__(self, valves_control):
        self.valves_control = valves_control

    def submit_valves_config(self, valves_config):
        try:
            self.valves_control.submit_valves_config(valves_config)
            return self._success_response()
        except Exception as error:
            return self.error_response(error)

    def _success_response(self, message='Operação concluída', data=''):
        return {'success': True, message: message, 'data': data}, 200

    def error_response(self, error):
        if type(error) is AppError:
            return {'success': False, 'key': error.origin, 'message': str(error)}
        return {'success': False,  'key': 'unkown', 'message': f'Erro desconhecido ({str(error)})'}
