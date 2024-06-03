
class ZeroObjectsDetected(Exception):
    def __init__(self):
        self.message = "Zero objects detected"
        # super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
