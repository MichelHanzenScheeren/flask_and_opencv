from app.errors.app_error import AppError
from app.models.webcam import Webcam
from app.models.analyze import Analyze


class AppUseCase():
    def __init__(self):
        self.webcam = Webcam()
        self.analyze = Analyze()
        # self._non_recoverable_error = non_recoverable_error

    def init_webcam(self):
        self.webcam.init_webcam()
        return self.webcam.video_status_and_port(), self.webcam.webcans_list()

    def save_uploaded_image(self, file):
        try:
            self.webcam.save_uploaded_image(file)
            return self._success_response(message='Imagem salva!')
        except Exception as error:
            message = f'Não foi possível salvar a imagem. (ERRO: {str(error)}'
            return self._error_response(AppError('save_uploaded_image', message))

    def define_points_of_rectangle(self, x1, y1, x2, y2):
        try:
            self.webcam.rectangle.define_points_of_rectangle(x1, y1, x2, y2)
            return self._success_response(message='Retângulo definido!')
        except Exception as error:
            message = f'Não foi possível definir o retângulo. (ERRO: {str(error)}'
            return self._error_response(AppError('define_points_of_rectangle', message))

    def clear_rectangle_and_uploaded_image(self):
        try:
            self.webcam.clear_rectangle_and_uploaded_image()
            return self._success_response()
        except Exception as error:
            message = f'Não foi possível concluir a solicitação. (ERRO: {str(error)}'
            return self._error_response(AppError('clear_rectangle_and_uploaded_image', message))

    def change_current_webcam(self, index):
        try:
            if index is None or (type(index) is not int) or index < 0:
                return self._error_response(AppError('change_current_webcam', 'Índice de webcam inválido'))
            data = self.webcam.change_current_webcam(index)
            return self._success_response(message='Webcam atual alterada', data=data)
        except Exception as error:
            message = f'Não foi possível alterar a webcam atual. (ERRO: {str(error)}'
            return self._error_response(AppError('change_current_webcam', message))

    def _success_response(self, message='Operação concluída', data=''):
        return {'success': True, 'message': message, 'data': data}

    def _error_response(self, error):
        if type(error) is AppError:
            return {'success': False, 'key': error.origin, 'message': str(error)}
        return {'success': False, 'key': 'unkown', 'message': f'Erro desconhecido ({str(error)})'}

    # def _non_recoverable_error_response(self):
    #     return self._non_recoverable_error()
