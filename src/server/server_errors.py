class ExpectedQueryParameter(Exception):
    def __init__(self, aParameter):
        self.parameter = aParameter
        super().__init__()
