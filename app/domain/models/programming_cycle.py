class ProgrammingCycle():
    def __init__(self):
        self.information = []

    def register_information(self, cycle_sequence, start, end):
        self.information.append(ProgrammingCycleInformation(cycle_sequence, start, end))


class ProgrammingCycleInformation():
    def __init__(self, sequence, start, end):
        self.sequence = sequence
        self.start = start
        self.end = end
