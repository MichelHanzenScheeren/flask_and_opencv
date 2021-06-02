from app.domain.use_cases.response_use_case import ResponseUseCase
from app.domain.errors.app_error import AppError


class ValvesUseCase():
    def __init__(self, valves_control):
        self.valves_control = valves_control

    def submit_valves_config(self, valves_config):
        try:
            self.valves_control.submit_valves_config(valves_config)
            return ResponseUseCase.success_response()
        except Exception as error:
            return ResponseUseCase.error_response(error)
