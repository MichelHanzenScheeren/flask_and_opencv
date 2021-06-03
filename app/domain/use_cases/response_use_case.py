from app.domain.errors.app_error import AppError
from flask import abort


class ResponseUseCase():
    @staticmethod
    def success_response(message='Operação concluída', data=''):
        return {'success': True, message: message, 'data': data}

    @staticmethod
    def error_response(error):
        if type(error) is AppError:
            abort(400, description=str(error))
        abort(400, description=f'Um erro desconhecido ocorreu (descrição: {str(error)})')

    @staticmethod
    def redirect_to_error_page(error):
        if type(error) is AppError:
            abort(404, description=str(error))
        abort(404, description=f'Um erro desconhecido ocorreu (descrição: {str(error)})')
