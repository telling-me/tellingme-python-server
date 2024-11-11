class RecordDto:
    def __init__(self, count: int):
        self.count = count

    @classmethod
    def builder(cls, count: int) -> "RecordDto":
        return cls(count)
