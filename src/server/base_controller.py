from flask import request
from server.session_serialization import SessionSerializer
from server_model.auth_service import AuthService
from server_model.clock import Clock
from server_model.hash import ArgonHash
from server_model.id_generator import SecretIdGenerator
from server_model.result_service import ResultService
from server_model.user_base import NameTaken, UserBase, UserNotFound, WrongPassword, PasswordTooShort, PasswordTooLong
from server_model.user import NameTooShort, NameTooLong
from server_model.session_registry import SessionRegistry
from server.server_errors import ExpectedBodyParameter, ExpectedQueryParameter, ExpectedJSONDictAsBody
import json


class BaseController:
    def __init__(self, app, aBaseUrl, aDatabase):
        self.app = app
        self.database = aDatabase
        self.clock = Clock()
        self.sessionRegistry = SessionRegistry(self.clock, SecretIdGenerator())
        self.userBase = UserBase(self.sessionRegistry, ArgonHash())
        self.authService = AuthService(self.database, self.userBase, self.sessionRegistry)
        self.resultService = ResultService(self.database, self.authService, self.clock)

        self.app.add_url_rule(aBaseUrl + "", view_func=self.hello_world)
        self.app.add_url_rule(aBaseUrl + "register", view_func=self.register, methods=["POST"])
        self.app.register_error_handler(NameTaken, self.nameTakenHandler)
        self.app.register_error_handler(NameTooShort, self.nameTooShortHandler)
        self.app.register_error_handler(NameTooLong, self.nameTooLongHandler)
        self.app.register_error_handler(PasswordTooShort, self.passwordTooShortHandler)
        self.app.register_error_handler(PasswordTooLong, self.passwordTooLongHandler)

        self.app.add_url_rule(aBaseUrl + "login", view_func=self.login, methods=["POST"])
        self.app.register_error_handler(UserNotFound, self.userNotFoundHandler)
        self.app.register_error_handler(WrongPassword, self.wrongPasswordHandler)

        self.app.add_url_rule(aBaseUrl + "result", view_func=self.result, methods=["POST"])

    def hello_world(self):
        return "Hello, World!!"

    def register(self):
        body = request.get_json(silent=True)

        if not isinstance(body, dict):
            raise ExpectedJSONDictAsBody

        name = body.get("name")
        if not name:
            raise ExpectedBodyParameter("name")

        password = body.get("password")
        if not password:
            raise ExpectedBodyParameter("password")

        session = self.authService.register(name, password)

        return json.dumps(SessionSerializer(session).serialize())

    def login(self):
        body = request.get_json(silent=True)

        if not isinstance(body, dict):
            raise ExpectedJSONDictAsBody

        name = body.get("name")
        if not name:
            raise ExpectedBodyParameter("name")

        password = body.get("password")
        if not password:
            raise ExpectedBodyParameter("password")

        session = self.authService.login(name, password)

        return json.dumps(SessionSerializer(session).serialize())

    def result(self):
        sessionId = request.args.get("session")
        if not sessionId:
            raise ExpectedQueryParameter("session")

        body = request.get_json(silent=True)

        if not isinstance(body, dict):
            raise ExpectedJSONDictAsBody
        print(body)

        score = body.get("score")
        if score is None:
            raise ExpectedBodyParameter("score")

        level = body.get("level")
        if level is None:
            raise ExpectedBodyParameter("level")

        lines = body.get("lines")
        if lines is None:
            raise ExpectedBodyParameter("lines")

        time = body.get("time")
        if time is None:
            raise ExpectedBodyParameter("time")

        self.resultService.save(sessionId, score, level, lines, time)

        return "Time saved"

    def nameTakenHandler(self, error):
        return "Name already taken, pick another one", 400

    def nameTooShortHandler(self, error):
        return "The name is too short", 400

    def nameTooLongHandler(self, error):
        return "The name is too long", 400

    def passwordTooShortHandler(self, error):
        return "The password is too short", 400

    def passwordTooLongHandler(self, error):
        return "The password is too long", 400

    def userNotFoundHandler(self, error):
        return "User not found", 400

    def wrongPasswordHandler(self, error):
        return "Wrong password", 400
