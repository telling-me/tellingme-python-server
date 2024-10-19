class RecordDto:
    def __init__(self, count: int):
        self.count = count

    @classmethod
    def builder(cls, count: int):
        return cls(count)

    def build(self):
        return self
