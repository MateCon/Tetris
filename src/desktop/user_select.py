from desktop.desktop_component import DesktopComponent
from server.session_serialization import SessionDeserializer
from desktop.form_component import FormComponent, TextInputComponent, ButtonComponent
from desktop.area import Area
import threading
import requests
import json


class LoginComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aCellSize, aKeybindMapper, aPlayWithFunction, anExitFunction):
        self.cellSize = aCellSize
        self.applicationContext = anApplicationContext
        self.playWith = aPlayWithFunction

        self.nameInput = TextInputComponent(anApplicationContext, "Name")
        self.passwordInput = TextInputComponent(anApplicationContext, "Password")
        self.submitButton = ButtonComponent(anApplicationContext, "Submit", self.submit)
        self.inputs = [self.nameInput, self.passwordInput, self.submitButton]
        self.form = FormComponent(anApplicationContext, "Login", self.inputs, aKeybindMapper, anExitFunction)
        self.response = ""
        self.hasRegistered = False
        self.errorHappened = False

    def submit(self):
        name = self.nameInput.value()
        password = self.passwordInput.value()
        self.submitButton.disable()

        threading.Thread(
            target=lambda: self.login(name, password),
            daemon=True
        ).start()

    def login(self, aName, aPassword):
        body = {
            "name": aName,
            "password": aPassword
        }
        response = requests.post("https://tetris-production-8c02.up.railway.app/login", json=body, verify=False)
        self.response = response.content
        self.hasRegistered = True
        self.submitButton.enable()

    def draw(self, anArea):
        self.form.draw(anArea)
        if self.errorHappened:
            self.applicationContext.drawText(self.response, (255, 255, 255), 22, anArea.shifted(20, 200))

    def update(self, millisecondsSinceLastUpdate):
        self.form.update(millisecondsSinceLastUpdate)

        if self.hasRegistered:
            try:
                session = SessionDeserializer(json.loads(self.response)).deserialize()
                self.applicationContext.savedSessions.add(session)
                self.playWith(session)
            except Exception:
                self.hasRegistered = False
                self.errorHappened = True

    def destroy(self):
        self.form.destroy()


class RegisterComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aCellSize, aKeybindMapper, aPlayWithFunction, anExitFunction):
        self.cellSize = aCellSize
        self.applicationContext = anApplicationContext
        self.playWith = aPlayWithFunction

        self.nameInput = TextInputComponent(anApplicationContext, "Name")
        self.passwordInput = TextInputComponent(anApplicationContext, "Password")
        self.submitButton = ButtonComponent(anApplicationContext, "Submit", self.submit)
        self.inputs = [self.nameInput, self.passwordInput, self.submitButton]
        self.form = FormComponent(anApplicationContext, "Register", self.inputs, aKeybindMapper, anExitFunction)
        self.response = ""
        self.hasRegistered = False
        self.errorHappened = False

    def submit(self):
        name = self.nameInput.value()
        password = self.passwordInput.value()
        self.submitButton.disable()

        threading.Thread(
            target=lambda: self.register(name, password),
            daemon=True
        ).start()

    def register(self, aName, aPassword):
        body = {
            "name": aName,
            "password": aPassword
        }
        response = requests.post("https://tetris-production-8c02.up.railway.app/register", json=body, verify=False)
        self.response = response.content
        self.hasRegistered = True
        self.submitButton.enable()

    def draw(self, anArea):
        self.form.draw(anArea)
        if self.errorHappened:
            self.applicationContext.drawText(self.response, (255, 255, 255), 22, anArea.shifted(20, 200))

    def update(self, millisecondsSinceLastUpdate):
        self.form.update(millisecondsSinceLastUpdate)

        if self.hasRegistered:
            try:
                session = SessionDeserializer(json.loads(self.response)).deserialize()
                self.applicationContext.savedSessions.add(session)
                self.playWith(session)
            except Exception:
                self.hasRegistered = False
                self.errorHappened = True

    def destroy(self):
        self.form.destroy()


class UserSelectMenuComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aCellSize, aKeybindMapper, aFunctionToOpenLogin, aFunctionToOpenRegister, aPlayWithFunction, anExitFunction):
        self.applicationContext = anApplicationContext
        self.cellSize = aCellSize
        self.borderColor = (255, 255, 255)
        self.borderWidth = 2
        self.playWith = aPlayWithFunction
        self.buttons = [
            ButtonComponent(anApplicationContext, "Login", aFunctionToOpenLogin),
            ButtonComponent(anApplicationContext, "Register", aFunctionToOpenRegister)
        ]
        self.applicationContext.savedSessions.do(
            lambda session: self.buttons.insert(0,
                ButtonComponent(anApplicationContext, session.user().name(), lambda: self.loginWithSession(session))
            )
        )
        self.form = FormComponent(anApplicationContext, "Select User", self.buttons, aKeybindMapper, anExitFunction)

    def loginWithSession(self, aSession):
        if self.applicationContext.savedSessions.isUsing(aSession):
            for button in self.buttons:
                if button.name == aSession.user().name():
                    button.fail()
        else:
            self.playWith(aSession)

    def draw(self, anArea):
        self.form.draw(anArea)

    def update(self, millisecondsSinceLastUpdate):
        self.form.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.form.destroy()


class UserSelectComponent(DesktopComponent):
    def __init__(self, anApplicationContext, anAmmountOfRows, anAmmountOfCols, aCellSize, aKeybindMapper, aPlayWithFunction, anExitFunction):
        self.applicationContext = anApplicationContext
        self.rows = anAmmountOfRows
        self.cols = anAmmountOfCols
        self.cellSize = aCellSize
        self.keybindMapper = aKeybindMapper
        self.playWith = aPlayWithFunction
        self.exitFunction = anExitFunction
        self.borderColor = (255, 255, 255)
        self.borderWidth = 2
        self.openSelectMenu()

    def openSelectMenu(self):
        self.component = UserSelectMenuComponent(self.applicationContext, self.cellSize, self.keybindMapper, self.openLogin, self.openRegister, self.playWith, self.exitFunction)

    def area(self):
        return Area(0, 0, self.cellSize * self.cols, self.cellSize * (self.rows + 2))

    def centeredArea(self, anotherArea):
        return self.area().centeredAt(anotherArea)

    def areaWithoutVanishZone(self, anotherArea):
        centeredBoardArea = self.centeredArea(anotherArea)
        return Area(
            centeredBoardArea.x,
            centeredBoardArea.y + self.cellSize * 2,
            centeredBoardArea.width,
            centeredBoardArea.height - self.cellSize * 2
        )

    def openLogin(self):
        self.component.destroy()
        self.component = LoginComponent(self.applicationContext, self.cellSize, self.keybindMapper, self.playWith, self.openSelectMenu)

    def openRegister(self):
        self.component.destroy()
        self.component = RegisterComponent(self.applicationContext, self.cellSize, self.keybindMapper, self.playWith, self.openSelectMenu)

    def draw(self, anArea):
        centeredArea = self.areaWithoutVanishZone(anArea)
        self.drawBorderAround(centeredArea)
        self.component.draw(centeredArea)

    def update(self, millisecondsSinceLastUpdate):
        self.component.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.component.destroy()
