from server.base_controller import BaseController
from server.server_errors import ExpectedBodyParameter, ExpectedJSONDictAsBody


class SetupFlaskApplication:
    def __init__(self, app, aDatabase):
        self.app = app
        self.database = aDatabase
        self.app.register_error_handler(ExpectedBodyParameter, self.expectedBodyParameterHandler)
        self.app.register_error_handler(ExpectedJSONDictAsBody, self.expectedJSONDictASBodyHandler)

    def setup(self):
        self.baseController = BaseController(self.app, "/", self.database)

    def expectedBodyParameterHandler(self, error: ExpectedBodyParameter):
        return f"Expected body parameter {error.parameter}", 400

    def expectedQueryParameterHandler(self, error: ExpectedBodyParameter):
        return f"Expected query parameter {error.parameter}", 400

    def expectedJSONDictASBodyHandler(self, error: ExpectedBodyParameter):
        return "Expected the body to be a JSON dictionary", 400
