from app.domain.errors.app_error import AppError
from app.domain.models.webcam import Webcam
from app.domain.models.analyze import Analyze


class AppUseCase():
    def __init__(self):
        self.webcam = Webcam()
        self.analyze = Analyze()

    def init_webcam(self):
        self.webcam.init_webcam()
        return self.webcam.video_status_and_port(), self.webcam.webcans_list()

    def save_uploaded_image(self, file):
        try:
            self.webcam.save_uploaded_image(file)
            return self._success_response(message='Imagem salva!')
        except Exception as error:
            message = f'Não foi possível salvar a imagem. (ERRO: {str(error)}'
            return self.error_response(AppError('save_uploaded_image', message))

    def define_points_of_rectangle(self, x1, y1, x2, y2):
        try:
            self.webcam.rectangle.define_points_of_rectangle(x1, y1, x2, y2)
            return self._success_response(message='Retângulo definido!')
        except Exception as error:
            message = f'Não foi possível definir o retângulo. (ERRO: {str(error)}'
            return self.error_response(AppError('define_points_of_rectangle', message))

    def clear_rectangle_and_uploaded_image(self):
        try:
            self.webcam.clear_rectangle_and_uploaded_image()
            return self._success_response()
        except Exception as error:
            message = f'Não foi possível concluir a solicitação. (ERRO: {str(error)}'
            return self.error_response(AppError('clear_rectangle_and_uploaded_image', message))

    def change_current_webcam(self, index):
        try:
            if index is None or (type(index) is not int) or index < 0:
                return self.error_response(AppError('change_current_webcam', 'Índice de webcam inválido'))
            data = self.webcam.change_current_webcam(index)
            return self._success_response(message='Webcam atual alterada', data=data)
        except Exception as error:
            message = f'Não foi possível alterar a webcam atual. (ERRO: {str(error)}'
            return self.error_response(AppError('change_current_webcam', message))

    def calculate_differentiator(self):
        try:
            differentiator_image = self.webcam.get_differentiator_image()
            self.analyze.clear()
            data = self.analyze.calculate_differentiator(differentiator_image)
            return self._success_response(data=data)
        except Exception as error:
            message = f'Não foi possível obter o diferenciador. (ERRO: {str(error)}'
            return self.error_response(AppError('calculate_differentiator', message))

    def get_differentiator_image(self):
        return self.analyze.results.get_differentiator_image()

    def start_analyze(self, form):
        self.analyze.start_analyze(form, self.webcam.get_cropped_image)
        self.webcam.clear()

    def get_results(self):
        if len(self.analyze.results.signals) == 0:
            raise AppError('results', 'Nenhum resultado encontrado')
        return self.analyze.results

    def get_all_images(self):
        zip_file = self.analyze.results.get_all_images()
        headers = {'content-type': 'application/zip', 'format': 'base64', 'file-name': 'imagens.zip'}
        return zip_file, headers

    def get_xlsx_results(self):
        xlsx_file = self.analyze.results.get_xlsx_results()
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        headers = {'content-type': content_type, 'format': 'base64', 'file-name': 'resultados.xlsx'}
        return xlsx_file, headers

    def saveNewAnalyzeDate(self, newDate):
        try:
            self.analyze.results.saveNewAnalyzeDate(newDate)
            return self._success_response()
        except Exception as error:
            return self.error_response(error)

    def _success_response(self, message='Operação concluída', data=''):
        return {'message': message, 'data': data}, 200

    def error_response(self, error):
        if type(error) is AppError:
            return {'success': False, 'key': error.origin, 'message': str(error)}
        return {'key': 'unkown', 'message': f'Erro desconhecido ({str(error)})'}, 404
