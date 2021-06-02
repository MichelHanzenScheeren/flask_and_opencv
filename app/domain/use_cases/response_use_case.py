from app.domain.errors.app_error import AppError


class ResponseUseCase():
    @staticmethod
    def success_response(message='Operação concluída', data=''):
        return {'success': True, message: message, 'data': data}

    @staticmethod
    def error_response(error):
        if type(error) is AppError:
            return {'success': False, 'key': error.origin, 'message': str(error)}
        return {'success': False, 'key': 'unkown', 'message': f'Erro desconhecido ({str(error)})'}
