from app.domain.models.valves_control import ValvesControl
from app.domain.errors.app_error import AppError
from app.domain.models.webcam import Webcam
from app.domain.models.analyze import Analyze


class AnalyzeUseCase():
    def __init__(self, webcam):
        self.webcam = webcam
        self.analyze = Analyze()

    def calculate_differentiator(self):
        try:
            self.analyze.clear()
            differentiator_image = self.webcam.get_differentiator_image()
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
