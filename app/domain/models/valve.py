from app.domain.packs.gpio_pack import GpioPack


class Valve():
    def __init__(self, board_number, valve_number):
        self.board_number = board_number
        self.valve_number = valve_number
        self.gpio_pack = GpioPack
        self._is_open = False
        self._configure()

    def _configure(self):
        self.gpio_pack.define_out_mode(self.board_number)
        self.gpio_pack.close_valve(self.board_number)

    def is_open(self):
        return self._is_open

    def close_valve(self):
        if self.is_open():
            self.gpio_pack.close_valve(self.board_number)
            self._is_open = False

    def open_valve(self):
        if not self.is_open():
            self.gpio_pack.open_valve(self.board_number)
            self._is_open = True
