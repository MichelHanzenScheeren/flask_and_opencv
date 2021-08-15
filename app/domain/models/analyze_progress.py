class AnalyzeProgress:
    def __init__(self):
        self.initialize()

    def initialize(self, total=0, concluded=0, progress=0):
        self.total = total
        self.concluded = concluded
        self.progress = progress

    def increase_progress(self):
        self.concluded += 1
        self.progress = 0 if self.total == 0 else self.concluded * 100 / self.total

    def status(self):
        return {"progress": self.progress, "message": self.progress_message()}

    def progress_message(self):
        if self.progress == 0:
            return "Configurando análise..."
        elif self.progress < 100:
            return "Capturando dados..."
        return "Processando resultados..."
