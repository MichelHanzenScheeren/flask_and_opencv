from datetime import datetime

class Results():
    def __init__(self):
        self.differentiator = []
        self.captures = [] 
        self.signals = []
        self.captures_images = []
    

    def initialize_parameters(self, total_time, captures_seg, description):
        self.initial_date = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)
        self.description = description or ""
        self.captures.clear()
        self.signals.clear()
        self.captures_images.clear()
        
