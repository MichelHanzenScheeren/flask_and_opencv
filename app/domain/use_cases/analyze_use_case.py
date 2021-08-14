from app.domain.use_cases.response_use_case import ResponseUseCase
from app.domain.models.valves_control import ValvesControl
from app.domain.errors.app_error import AppError
from app.domain.models.webcam import Webcam
from app.domain.models.analyze import Analyze


class AnalyzeUseCase():
    def __init__(self, webcam, valves_control, analyze):
        self.webcam = webcam
        self.valves_control = valves_control
        self.analyze = analyze

    def calculate_differentiator(self):
        try:
            differentiator_image = self.webcam.get_differentiator_image()
            data = self.analyze.calculate_differentiator(differentiator_image)
            return ResponseUseCase.success_response(data=data)
        except Exception as error:
            message = f'Não foi possível obter o diferenciador. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('calculate_differentiator', message))

    def start_analyze(self, form):
        try:
            get_image = self.webcam.get_cropped_image
            programming_interpret = self.valves_control.start_programming_interpretation
            self.analyze.start_analyze(form, get_image, programming_interpret)
            self.webcam.clear()
        except Exception as error:
            message = f'Um erro interno impediu que a análise fosse concluída. (ERRO: {str(error)})'
            return ResponseUseCase.redirect_to_error_page(AppError('get_all_images', message))

    def get_results(self):
        try:
            if len(self.analyze.results.signals) == 0:
                raise AppError('get_results', 'Nenhum resultado foi encontrado.')
            return self.analyze.results
        except Exception as error:
            return ResponseUseCase.redirect_to_error_page(error)

    def get_all_images(self):
        try:
            zip_file = self.analyze.results.get_all_images()
            headers = {'content-type': 'application/zip', 'format': 'base64', 'file-name': 'imagens.zip'}
            return zip_file, headers
        except Exception as error:
            message = f'Não foi possível fazer o download do arquivo. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('get_all_images', message))

    def get_xlsx_results(self):
        try:
            xlsx_file = self.analyze.results.get_xlsx_results()
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            headers = {'content-type': content_type, 'format': 'base64', 'file-name': 'resultados.xlsx'}
            return xlsx_file, headers
        except Exception as error:
            message = f'Não foi possível fazer o download do arquivo. (ERRO: {str(error)})'
            return ResponseUseCase.error_response(AppError('get_xlsx_results', message))

    def save_new_analyze_date(self, newDate):
        try:
            self.analyze.results.save_new_analyze_date(newDate)
            return ResponseUseCase.success_response()
        except Exception as error:
            return ResponseUseCase.error_response(error)
