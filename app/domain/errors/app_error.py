class AppError(Exception):
    def __init__(self, origin, *args, **kwargs):
        super(AppError, self).__init__(*args, **kwargs)
        self.origin = origin
