class ExpectedJSONDictAsBody(Exception):
    pass


class ExpectedBodyParameter(Exception):
    def __init__(self, aParameter):
        self.parameter = aParameter
        super().__init__()


class ExpectedQueryParameter(Exception):
    def __init__(self, aParameter):
        self.parameter = aParameter
        super().__init__()
