from app.domain.models.create_html_from_programming import CreateHtmlFromProgramming
from app.domain.models.save_json_programming import SaveJsonProgramming
from app.domain.errors.app_error import AppError
from app.configuration import NUMBER_OF_VALVES, VALVE_MAPPING, BOARD_NUMBER, VALVE_NUMBER
from app.domain.packs.gpio_pack import GpioPack
from app.domain.models.valve import Valve


class ValvesControl():
    def __init__(self):
        GpioPack.set_board_pinout()  # Define o modo de controle dos pinos do raspberry
        self.valves = []
        self._initialize_valves()

    def _initialize_valves(self):
        for map in VALVE_MAPPING:
            valve = Valve(map[BOARD_NUMBER], map[VALVE_NUMBER])
            self.valves.append(valve)

    def submit_valves_config(self, valves_config):
        self._validate_valves_config(valves_config)
        if len(valves_config) > 0:
            self._apply_valves_config(valves_config)

    def _validate_valves_config(self, valves_config):
        key = 'ValvesControl.submit_valves_config'
        if type(valves_config) is not list:
            raise AppError(key, 'Lista de configuração inválida')
        if len(valves_config) > NUMBER_OF_VALVES:
            raise AppError(key, 'Quantidade inválida de válvulas')
        for valve in valves_config:
            if type(valve) is not int or valve < 0 or valve > NUMBER_OF_VALVES:
                raise AppError(key, 'Uma ou mais válvulas são inválidas')

    def _apply_valves_config(self, valves_config):
        for valve in self.valves:
            if valve.valve_number in valves_config:
                valve.open_valve()
            else:
                valve.close_valve()

    def submit_programming(self, dictionary):
        SaveJsonProgramming(dictionary).create()

    def create_html_from_programming(self, dictionary):
        html_creator = CreateHtmlFromProgramming(dictionary)
        return html_creator.create()

    def __del__(self):
        GpioPack.cleanup()  # Libera os pinos do raspberry
