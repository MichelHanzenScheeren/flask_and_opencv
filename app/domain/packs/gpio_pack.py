# import RPi.GPIO as gpio


class GpioPack():
    """ Classe de métodos estáticos que encapsula todas as chamadas diretas a biblioteca RPI.GPIO.
    A biblioteca RPI.GPIO cuida do INPUT e OUTPUT dos pinos do raspberry pi.
    """

    @staticmethod
    def set_board_pinout():
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)

    @staticmethod
    def define_out_mode(board_number):
        gpio.setup(board_number, gpio.OUT)

    @staticmethod
    def close_valve(board_number):
        gpio.output(board_number, gpio.HIGH)

    @staticmethod
    def close_value():
        return gpio.HIGH

    @staticmethod
    def open_valve(board_number):
        gpio.output(board_number, gpio.LOW)

    @staticmethod
    def open_value():
        return gpio.LOW

    @staticmethod
    def multiple_open_close(board_numbers, situations):
        gpio.output(board_numbers, situations)

    @staticmethod
    def cleanup():
        gpio.cleanup()


# Usado apenas porque não existe o pacote RPI.GPIO para Windows
class gpio():
    """ Classe de métodos estáticos auxiliar criada para simular as chamada a biblioteca RPI.GPIO.

    Sua criação foi necessária pois o desenvolvimento da aplicação foi feito no windows, que não
    possui a biblioteca RPI.GPIO.
    """

    BOARD, OUT, HIGH, LOW = '', '', '', ''

    @staticmethod
    def setwarnings(_):
        pass

    @staticmethod
    def setmode(_):
        pass

    @staticmethod
    def setup(_, __):
        pass

    @staticmethod
    def output(_, __):
        pass

    @staticmethod
    def cleanup():
        pass
