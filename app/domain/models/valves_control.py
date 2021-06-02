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

    def __del__(self):
        GpioPack.cleanup()  # Libera os pinos do raspberry
