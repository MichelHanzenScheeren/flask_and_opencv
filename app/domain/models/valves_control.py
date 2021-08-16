from datetime import datetime
from time import sleep
from app.configuration import JSON_PROGRAMMING_PATH, NUMBER_OF_VALVES, PARTIAL_JSON_PROGRAMMING_PATH, VALVE_MAPPING, BOARD_NUMBER, VALVE_NUMBER
from app.domain.packs.gpio_pack import GpioPack
from app.domain.errors.app_error import AppError
from app.domain.models.programming import Programming
from app.domain.models.create_html_from_programming import CreateHtmlFromProgramming
from app.domain.models.save_json_programming import SaveJsonProgramming
from app.domain.models.valve import Valve
from app.domain.packs.json_pack import JsonPack
from app.domain.models.programming_cycle import ProgrammingCycle


class ValvesControl():
    def __init__(self):
        GpioPack.set_board_pinout()  # Define o modo de controle dos pinos do raspberry
        self.valves = []
        self.interpretation = []
        self._initialize_valves()

    def _initialize_valves(self):
        for map in VALVE_MAPPING:
            valve = Valve(map[BOARD_NUMBER], map[VALVE_NUMBER])
            self.valves.append(valve)

    def submit_valves_config(self, valves_config):
        self._validate_valves_config(valves_config)
        self.apply_valves_config(valves_config)

    def _validate_valves_config(self, valves_config):
        key = 'ValvesControl.submit_valves_config'
        if type(valves_config) is not list:
            raise AppError(key, 'Lista de configuração inválida')
        if len(valves_config) > NUMBER_OF_VALVES:
            raise AppError(key, 'Quantidade inválida de válvulas')
        for valve in valves_config:
            if type(valve) is not int or valve < 0 or valve > NUMBER_OF_VALVES:
                raise AppError(key, 'Uma ou mais válvulas são inválidas')

    def apply_valves_config(self, valves_config):
        numbers, situation = [], []
        for valve in self.valves:
            numbers.append(valve.board_number)
            if valve.valve_number in valves_config:
                situation.append(GpioPack.open_value())
            else:
                situation.append(GpioPack.close_value())
        GpioPack.multiple_open_close(numbers, situation)

    def save_json_programming(self, dictionary):
        self.convert_dictionary_programming(dictionary)  # Vai validar se está tudo ok
        save_json = SaveJsonProgramming(dictionary)
        save_json.create()

    def convert_dictionary_programming(self, dictionary):
        programming = Programming().from_dictionary(dictionary)
        return programming

    def create_html_from_programming_dictionary(self, dictionary):
        html_creator = CreateHtmlFromProgramming(dictionary)
        return html_creator.create()

    def start_programming_interpretation(self, progress):
        self.interpretation = []
        json = JsonPack.read(JSON_PROGRAMMING_PATH)
        program = Programming().from_dictionary(json)
        self.interpret_programming(program, progress)

    def interpret_programming(self, program, analyze_progress):
        total = 0
        for group in program.valves_program:
            executed_ids = []
            for index, line in enumerate(group.lines):
                if line.line_number in executed_ids:
                    continue
                if program.triplicate and line.cycle_start:
                    cycle_lines = self._build_cycle_list(index, group.lines, executed_ids)
                    total += (len(cycle_lines) * 3)
                    self.interpretation.append(cycle_lines)
                else:
                    self.interpretation.append(line)
                    total += 1
        analyze_progress.initialize(total)

    def _build_cycle_list(self, current_index, lines, executed_ids):
        elements = [lines[current_index]]
        if current_index + 1 < len(lines):
            for line in lines[current_index + 1:]:
                if line.cycle_start:
                    break
                executed_ids.append(line.line_number)
                elements.append(line)
        return elements

    def execute_interpretation(self, cycles_information, analyze_progress):
        for element in self.interpretation:
            if isinstance(element, list):
                self._execute_cycle(element, cycles_information, analyze_progress)
            else:
                self._execute_line(element, analyze_progress)
        self.close_all_valves()

    def _execute_cycle(self, lines, cycles_information, analyze_progress):
        cycle = ProgrammingCycle()
        for index in range(0, 3):
            start = datetime.now()
            for element in lines:
                self._execute_line(element, analyze_progress)
            cycle.register_information(index, start, datetime.now())
        cycles_information.append(cycle)

    def _execute_line(self, line, analyze_progress):
        self.apply_valves_config(line.open_valves)
        sleep(line.sleep_time)
        analyze_progress.increase_progress()

    def close_all_valves(self):
        self.apply_valves_config([])

    def validate_file_and_return_programming_path(self):
        JsonPack.read(JSON_PROGRAMMING_PATH)  # dispara um erro se não existir
        return PARTIAL_JSON_PROGRAMMING_PATH

    def __del__(self):
        GpioPack.cleanup()  # Libera os pinos do raspberry
