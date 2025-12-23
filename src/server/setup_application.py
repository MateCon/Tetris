from server.base_section import BaseSection
from server.server_errors import ExpectedQueryParameter


class SetupFlaskApplication:
    def __init__(self, app, aDatabase):
        self.app = app
        self.database = aDatabase
        self.app.register_error_handler(ExpectedQueryParameter, self.expectedQueryParameterHandler)

    def setup(self):
        self.baseSection = BaseSection(self.app, "/", self.database)

    def expectedQueryParameterHandler(self, error: ExpectedQueryParameter):
        return f"Expecter query parameter {error.parameter}", 400
