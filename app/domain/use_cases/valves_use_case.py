from app.domain.use_cases.response_use_case import ResponseUseCase


class ValvesUseCase():
    def __init__(self, valves_control):
        self.valves_control = valves_control

    def submit_valves_config(self, valves_config):
        try:
            self.valves_control.submit_valves_config(valves_config)
            return ResponseUseCase.success_response()
        except Exception as error:
            return ResponseUseCase.error_response(error)

    def submit_programming(self, dictionary):
        try:
            self.valves_control.submit_programming(dictionary)
            return ResponseUseCase.success_response(message='Programação salva com sucesso')
        except Exception as error:
            return ResponseUseCase.error_response(error)

    def upload_user_programming(self, dictionary):
        try:
            self.valves_control.submit_programming(dictionary)
            html = self.valves_control.create_html_from_programming(dictionary)
            return ResponseUseCase.success_response(data=html)
        except Exception as error:
            return ResponseUseCase.error_response(error)
