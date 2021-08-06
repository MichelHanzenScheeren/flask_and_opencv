# FPS das capturas da webcam: (+/- 24 fps)
FRAME_RATE = 0.04

# Caminho do arquivo de programação usado
JSON_PROGRAMMING_PATH = 'app/static/files/programming.json'
PARTIAL_JSON_PROGRAMMING_PATH = 'static/files/programming.json'

# Número de válvulas utilizadas na aplicação
NUMBER_OF_VALVES = 16

# Propriedades da configuação de Válvulas
BOARD_NUMBER = 'board_number'
VALVE_NUMBER = 'valve_number'

# Configuração das válvulas usadas na aplicação
VALVE_MAPPING = [
    {BOARD_NUMBER: 11, VALVE_NUMBER: 1},
    {BOARD_NUMBER: 12, VALVE_NUMBER: 2},
    {BOARD_NUMBER: 13, VALVE_NUMBER: 3},
    {BOARD_NUMBER: 15, VALVE_NUMBER: 4},
    {BOARD_NUMBER: 16, VALVE_NUMBER: 5},
    {BOARD_NUMBER: 18, VALVE_NUMBER: 6},
    {BOARD_NUMBER: 22, VALVE_NUMBER: 7},
    {BOARD_NUMBER: 29, VALVE_NUMBER: 8},

    {BOARD_NUMBER: 31, VALVE_NUMBER: 9},
    {BOARD_NUMBER: 32, VALVE_NUMBER: 10},
    {BOARD_NUMBER: 33, VALVE_NUMBER: 11},
    {BOARD_NUMBER: 35, VALVE_NUMBER: 12},
    {BOARD_NUMBER: 36, VALVE_NUMBER: 13},
    {BOARD_NUMBER: 37, VALVE_NUMBER: 14},
    {BOARD_NUMBER: 38, VALVE_NUMBER: 15},
    {BOARD_NUMBER: 40, VALVE_NUMBER: 16},
]

# Propriedadas do arquivo de programação
SAVED_DATE = 'data'
SUBTITLE = 'legenda'
PROGRAMMING = 'programacao'
GROUP_NUMBER = 'grupo_'
LINE_NUMBER = 'linha_'
CYCLE_START = 'inicio_ciclo'
SLEEP_TIME = 'tempo_espera'
OPEN_VALVES = 'valvulas_abertas'
VALVES_QUANTITY = 'qtd_valvulas'
WORKING_IN_TRIPLICATE = 'triplicata'
KEY_SEPARATOR = '_'

# Formato String padrão usado para transformar datetime para string e/ou de string
STRING_FORMAT = '%d-%m-%Y %H:%M:%S'
