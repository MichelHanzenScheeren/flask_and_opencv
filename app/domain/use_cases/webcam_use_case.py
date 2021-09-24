from app.domain.models.webcam_configuration import WebcamConfiguration
from app.domain.use_cases.response_use_case import ResponseUseCase
from app.configuration import NUMBER_OF_VALVES
from app.domain.errors.app_error import AppError
import json


class WebcamUseCase():
    def __init__(self, webcam, analyze):
        self.webcam = webcam
        self.analyze = analyze

    def initialize_and_get_parameters(self):
        try:
            WebcamConfiguration(self.webcam.current_port).apply_current_config()
            self.analyze.clear()
            self.webcam.init_webcam()
            index_parameters = self.webcam.video_status_and_port()
            index_parameters['webcans_list'] = self.webcam.webcans_list()
            index_parameters['valves_number'] = NUMBER_OF_VALVES
            index_parameters['differentiator'] = json.dumps(self.analyze.differentiator_values())
            index_parameters['rectangle'] = json.dumps(self.webcam.rectangle.rectangle_values())
            index_parameters['total_time'] = self.analyze.results.total_time
            index_parameters['qtd'] = self.analyze.results.captures_seg
            return index_parameters
        except Exception as error:
            message = f'Um erro ocorreu quando tentávamos configurar sua webcam. (ERRO: {str(error)})'
            return ResponseUseCase.redirect_to_error_page(AppError('init_webcam_and_get_parameters', message))

    def save_uploaded_image(self, file):
        try:
            self.webcam.save_uploaded_image(file)
            return ResponseUseCase.success_response(message='Imagem salva!')
        except Exception as error:
            message = f'Não foi possível salvar a imagem. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('save_uploaded_image', message))

    def define_points_of_rectangle(self, x1, y1, x2, y2):
        try:
            self.webcam.rectangle.define_points_of_rectangle(x1, y1, x2, y2)
            return ResponseUseCase.success_response(message='Retângulo definido!')
        except Exception as error:
            message = f'Não foi possível definir o retângulo. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('define_points_of_rectangle', message))

    def clear_uploaded_image(self):
        try:
            self.webcam.clear_uploaded_image()
            return ResponseUseCase.success_response()
        except Exception as error:
            message = f'Não foi possível concluir a solicitação. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('clear_rectangle_and_uploaded_image', message))

    def clear_rectangle(self):
        try:
            self.webcam.clear_rectangle()
            return ResponseUseCase.success_response()
        except Exception as error:
            message = f'Não foi possível concluir a solicitação. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('clear_rectangle_and_uploaded_image', message))

    def change_current_webcam(self, index):
        try:
            if index is None or (type(index) is not int) or index < 0:
                return ResponseUseCase.error_response(AppError('change_current_webcam', 'Índice de webcam inválido'))
            data = self.webcam.change_current_webcam(index)
            return ResponseUseCase.success_response(message='Webcam atual alterada', data=data)
        except Exception as error:
            message = f'Não foi possível alterar a webcam atual. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('change_current_webcam', message))

    def configure_webcam(self):
        try:
            WebcamConfiguration(self.webcam.current_port).auto_config()
            return ResponseUseCase.success_response(message='Webcam atual configurada')
        except Exception as error:
            message = f'Não foi possível concluir a configuração automática da webcam. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('configure_webcam', message))
