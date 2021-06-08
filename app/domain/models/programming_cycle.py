class ProgrammingCycle():
    def __init__(self, group_sequence, start_sequence, end_sequence):
        self.group_sequence = group_sequence
        self.start_sequence = start_sequence
        self.end_sequence = end_sequence
        self.information = []

    def register_information(self, cycle_sequence, start, end):
        self.information.append(ProgrammingCycleInformation(cycle_sequence, start, end))


class ProgrammingCycleInformation():
    def __init__(self, sequence, start, end):
        self.sequence = sequence
        self.start = start
        self.end = end
