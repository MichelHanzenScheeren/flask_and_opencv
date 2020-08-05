class Results():
    def __init__(self):
        self.differentiator = []
        self.captures = []
        self.signals = []
        self.total_time = 0
        self.captures_seg = 1
    
    def save_results(self, differentiator, captures, signals, total_time, captures_seg, interval):
        self.differentiator = differentiator
        self.captures = captures
        self.signals = signals
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = interval