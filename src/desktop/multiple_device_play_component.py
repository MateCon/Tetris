from pygame.joystick import Joystick
from desktop.desktop_component import DesktopComponent
from desktop.area import Area
from desktop.color_scheme import ColorScheme
from desktop.held_command_repeater import HeldCommandRepeater
from tetris_model.tetris_event_notifier import TetrisEventNotifier
from tetris_model.tetris_game import TetrisGame
from tetris_model.rotation_list_generator import NintendoRotationListGenerator, SegaRotationListGenerator, SuperRotationListGenerator
from tetris_model.kicks import SRSKicks
from tetris_model.rand import Rand
from tetris_model.point import Point
from desktop.game_component import GameComponent
from server_model.session import Session
from server_model.user import User
from abc import abstractmethod
from datetime import datetime, timedelta
import pygame
import threading
import requests
import json


class LoginComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aCellSize, aKeybindMapper, aPlayWithFunction):
        self.cellSize = aCellSize
        self.applicationContext = anApplicationContext
        self.playWith = aPlayWithFunction

        self.nameInput = TextInputComponent(anApplicationContext, "Name")
        self.passwordInput = TextInputComponent(anApplicationContext, "Password")
        self.submitButton = ButtonComponent(anApplicationContext, "Submit", self.submit)
        self.inputs = [self.nameInput, self.passwordInput, self.submitButton]
        self.form = FormComponent(anApplicationContext, "Login", self.inputs, aKeybindMapper)
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
        response = requests.post("https://127.0.0.1:5000/login", json=body, verify=False)
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
                body = json.loads(self.response)
                sessionDictionary = body.get("session")
                user = User(sessionDictionary.get("user_name"), "")
                session = Session(
                    sessionDictionary.get("id"),
                    user,
                    datetime.fromisoformat(sessionDictionary.get("creation_date")),
                    timedelta(seconds=int(sessionDictionary.get("duration")))
                )
                self.applicationContext.savedSessions.add(session)
                self.playWith(session)
            except Exception:
                self.hasRegistered = False
                self.errorHappened = True

    def destroy(self):
        self.form.destroy()


class RegisterComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aCellSize, aKeybindMapper, aPlayWithFunction):
        self.cellSize = aCellSize
        self.applicationContext = anApplicationContext
        self.playWith = aPlayWithFunction

        self.nameInput = TextInputComponent(anApplicationContext, "Name")
        self.passwordInput = TextInputComponent(anApplicationContext, "Password")
        self.submitButton = ButtonComponent(anApplicationContext, "Submit", self.submit)
        self.inputs = [self.nameInput, self.passwordInput, self.submitButton]
        self.form = FormComponent(anApplicationContext, "Register", self.inputs, aKeybindMapper)
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
        response = requests.post("https://127.0.0.1:5000/register", json=body, verify=False)
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
                body = json.loads(self.response)
                sessionDictionary = body.get("session")
                user = User(sessionDictionary.get("user_name"), "")
                session = Session(
                    sessionDictionary.get("id"),
                    user,
                    datetime.fromisoformat(sessionDictionary.get("creation_date")),
                    timedelta(seconds=int(sessionDictionary.get("duration")))
                )
                self.applicationContext.savedSessions.add(session)
                self.playWith(session)
            except Exception:
                self.hasRegistered = False
                self.errorHappened = True

    def destroy(self):
        self.form.destroy()



class VirtualKeyboardComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self._isOpen = False
        self.borderWidth = 2
        self.keys = [
            ["1","2","3","4","5","6","7","8","9","0"],
            ["q","w","e","r","t","y","u","i","o","p"],
            ["a","s","d","f","g","h","j","k","l", "<"],
            ["z","x","c","v","b","n","m", "accept"]
        ]
        self.position = Point(0, 2)

    def isOpen(self):
        return self._isOpen

    def openWith(self, anInput):
        self.position = Point(0, 2)
        self._isOpen = True
        self._input = anInput

    def close(self):
        self._isOpen = False
        self._input.stopEditing()

    def moveUp(self):
        self.position.y = (self.position.y - 1) % len(self.keys)

    def moveDown(self):
        self.position.y = (self.position.y + 1) % len(self.keys)

    def realPosition(self):
        return Point(min(self.position.x, len(self.keys[self.position.y]) - 1), self.position.y)

    def moveLeft(self):
        self.position.x = (self.realPosition().x - 1) % len(self.keys[self.position.y])

    def moveRight(self):
        self.position.x = (self.realPosition().x + 1) % len(self.keys[self.position.y])

    def accept(self):
        key = self.keys[self.realPosition().y][self.realPosition().x]
        if key == "<":
            self._input.delete()
        elif key == "accept":
            self._input.closeKeyboard()
        else:
            self._input.write(key)

    def draw(self, anArea):
        if not self._isOpen:
            return
        self.drawBorderAround(anArea)
        keySize = Point(anArea.width // 10, anArea.height // 4)
        keyArea = Area(0, 0, keySize.x, keySize.y)
        for y, row in enumerate(self.keys):
            for x, key in enumerate(row):
                currentArea = anArea.shifted(x * keySize.x, y * keySize.y)
                currentArea.width = keyArea.width
                currentArea.height = keyArea.height
                if Point(x, y) == self.realPosition():
                    if key == "accept":
                        currentArea.width *= 3
                    self.applicationContext.drawArea((255, 255, 255), currentArea)
                    textColor = (0, 0, 0)
                else:
                    light = 255 - ((abs(x - self.realPosition().x) + abs(y - self.realPosition().y)) * 20)
                    textColor = (light, light, light)
                self.applicationContext.drawText(key, textColor, 22, currentArea.shifted(8, 0))

    def update(self, millisecondsSinceLastUpdate):
        pass


class FormComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aTitle, aListOfInputs, aKeybindMapper):
        assert len(aListOfInputs) > 0
        self.applicationContext = anApplicationContext
        self.title = aTitle
        self.inputs = aListOfInputs
        self.currentInputIndex = 0
        self.inputs[0].focus()
        self.virtualKeyboard = VirtualKeyboardComponent(anApplicationContext)
        self.leftCommandRepeater = HeldCommandRepeater(self.moveLeft, 250, 75)
        self.rightCommandRepeater = HeldCommandRepeater(self.moveRight, 250, 75)
        self.upCommandRepeater = HeldCommandRepeater(self.moveUp, 250, 75)
        self.downCommandRepeater = HeldCommandRepeater(self.moveDown, 250, 75)
        aKeybindMapper(self)

    def startMovingDown(self):
        self.downCommandRepeater.start()

    def stopMovingDown(self):
        self.downCommandRepeater.stop()

    def startMovingUp(self):
        self.upCommandRepeater.start()

    def stopMovingUp(self):
        self.upCommandRepeater.stop()

    def startMovingLeft(self):
        self.leftCommandRepeater.start()

    def stopMovingLeft(self):
        self.leftCommandRepeater.stop()

    def startMovingRight(self):
        self.rightCommandRepeater.start()

    def stopMovingRight(self):
        self.rightCommandRepeater.stop()

    def exit(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.close()
        else:
            pass

    def moveDown(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveDown()
        else:
            self.inputs[self.currentInputIndex].unfocus()
            self.currentInputIndex += 1
            self.currentInputIndex = self.currentInputIndex % len(self.inputs)
            self.inputs[self.currentInputIndex].focus()

    def moveUp(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveUp()
        else:
            self.inputs[self.currentInputIndex].unfocus()
            self.currentInputIndex -= 1
            self.currentInputIndex = self.currentInputIndex % len(self.inputs)
            self.inputs[self.currentInputIndex].focus()

    def moveLeft(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveLeft()

    def moveRight(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.moveRight()

    def accept(self):
        if self.virtualKeyboard.isOpen():
            self.virtualKeyboard.accept()
        else:
            self.inputs[self.currentInputIndex].accept(self)

    def openVirtualKeyboardWith(self, anInput):
        self.virtualKeyboard.openWith(anInput)

    def closeVirtualKeyboard(self):
        self.virtualKeyboard.close()

    def draw(self, anArea):
        currentArea = anArea.copy()
        currentArea.height = 40
        self.applicationContext.drawText(self.title, (255, 255, 255), 38, currentArea.shifted(20, 0))
        currentArea = currentArea.shifted(0, 50)
        currentArea.height = 30
        for input in self.inputs:
            input.draw(currentArea)
            currentArea = currentArea.shifted(0, 30)

        keyboardHeight = anArea.width // 10 * 4
        self.virtualKeyboard.draw(Area(anArea.x, anArea.y + anArea.height - keyboardHeight, anArea.width, keyboardHeight))

    def update(self, millisecondsSinceLastUpdate):
        self.leftCommandRepeater.update(millisecondsSinceLastUpdate)
        self.rightCommandRepeater.update(millisecondsSinceLastUpdate)
        self.upCommandRepeater.update(millisecondsSinceLastUpdate)
        self.downCommandRepeater.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.applicationContext.inputObserver.removeFrom(self)


class InputComponent(DesktopComponent):
    @abstractmethod
    def focus(self):
        pass

    @abstractmethod
    def unfocus(self):
        pass

    @abstractmethod
    def accept(self, aForm):
        pass


class ButtonComponent(InputComponent):
    def __init__(self, anApplicationContext, aName, anAction):
        self.applicationContext = anApplicationContext
        self.name = aName
        self.action = anAction
        self.focused = False
        self.enabled = True

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

    def accept(self, aForm):
        if self.enabled:
            self.action()

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def draw(self, anArea):
        if self.focused:
            textColor = (0, 0, 0)
            rectColor = (255, 255, 255)
            if not self.enabled:
                rectColor = (100, 100, 100)
        else:
            textColor = (255, 255, 255)
            rectColor = (0, 0, 0)
        self.applicationContext.drawArea(rectColor, anArea)
        self.applicationContext.drawText(self.name, textColor, 24, anArea.withPadding(20, 0))

    def update(self, millisecondsSinceLastUpdate):
        pass


class TextInputComponent(InputComponent):
    def __init__(self, anApplicationContext, aName):
        self.applicationContext = anApplicationContext
        self.name = aName
        self.focused = False
        self.borderWidth = 2
        self.text = ""
        self.editing = False

    def value(self):
        return self.text

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

    def accept(self, aForm):
        self.form = aForm
        self.form.openVirtualKeyboardWith(self)
        self.editing = True

    def delete(self):
        self.text = self.text[0:-1]

    def closeKeyboard(self):
        self.form.closeVirtualKeyboard()

    def stopEditing(self):
        self.editing = False

    def write(self, aString):
        self.text += aString

    def draw(self, anArea):
        if self.focused:
            textColor = (255, 255, 255)
            outerAreaColor = (255, 255, 255)
            innerAreaColor = (0, 0, 0)
        else:
            textColor = (0, 0, 0)
            outerAreaColor = (0, 0, 0)
            innerAreaColor = (255, 255, 255)

        self.applicationContext.drawArea(outerAreaColor, anArea)
        self.applicationContext.drawArea(innerAreaColor, anArea.withPadding(15, 3))

        text = self.text
        if self.text == "" and not self.editing:
            text = self.name
            textColor = (150, 150, 150)

        currentArea = anArea.withPadding(20, 0)
        for c in text:
            self.applicationContext.drawText(c, textColor, 24, currentArea)
            currentArea = currentArea.shifted(12, 0)

        if self.editing:
            cursor = currentArea.copy().shifted(0, 6)
            cursor.width = 10
            cursor.height = 18
            self.applicationContext.drawArea(textColor, cursor)

    def update(self, millisecondsSinceLastUpdate):
        pass


class UserSelectMenuComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aCellSize, aKeybindMapper, aFunctionToOpenLogin, aFunctionToOpenRegister, aPlayWithFunction):
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
        self.form = FormComponent(anApplicationContext, "Select User", self.buttons, aKeybindMapper)

    def loginWithSession(self, aSession):
        self.playWith(aSession)

    def draw(self, anArea):
        self.form.draw(anArea)

    def update(self, millisecondsSinceLastUpdate):
        self.form.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.form.destroy()


class UserSelectComponent(DesktopComponent):
    def __init__(self, anApplicationContext, anAmmountOfRows, anAmmountOfCols, aCellSize, aKeybindMapper, aPlayWithFunction):
        self.applicationContext = anApplicationContext
        self.rows = anAmmountOfRows
        self.cols = anAmmountOfCols
        self.cellSize = aCellSize
        self.keybindMapper = aKeybindMapper
        self.playWith = aPlayWithFunction
        self.borderColor = (255, 255, 255)
        self.borderWidth = 2
        self.component = UserSelectMenuComponent(anApplicationContext, aCellSize, aKeybindMapper, self.openLogin, self.openRegister, self.playWith)

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
        self.component = LoginComponent(self.applicationContext, self.cellSize, self.keybindMapper, self.playWith)

    def openRegister(self):
        self.component.destroy()
        self.component = RegisterComponent(self.applicationContext, self.cellSize, self.keybindMapper, self.playWith)

    def draw(self, anArea):
        centeredArea = self.areaWithoutVanishZone(anArea)
        self.drawBorderAround(centeredArea)
        self.component.draw(centeredArea)

    def update(self, millisecondsSinceLastUpdate):
        self.component.update(millisecondsSinceLastUpdate)


class DeviceComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aDevice, aDeletionFunction):
        self.applicationContext = anApplicationContext
        self.device = aDevice
        self.deletionFunction = aDeletionFunction
        self.rows = 20
        self.cols = 10
        self.cellSize = 25
        self.component = self.createUserSelectComponent()

    def createUserSelectComponent(self):
        return UserSelectComponent(
            self.applicationContext,
            self.rows,
            self.cols,
            self.cellSize,
            self.mapUserSelectComponent,
            self.playWith
        )

    def playWith(self, aSession):
        self.session = aSession
        self.component = self.createGameComponent()

    def createGameComponent(self):
        tetrisEventNotifier = TetrisEventNotifier()
        game = TetrisGame(
            self.cols,
            self.rows,
            Rand(),
            SuperRotationListGenerator,
            SRSKicks,
            tetrisEventNotifier
        )
        return GameComponent(
            self.applicationContext,
            game,
            self.rows,
            self.cols,
            self.cellSize,
            tetrisEventNotifier,
            self.mapGameComponent,
            ColorScheme(),
            self.restartGame,
            self.deleteGame,
            self.session
        )

    def deleteGame(self):
        self.deletionFunction()

    def restartGame(self):
        self.unmap()
        self.component = self.createGameComponent()

    def mapKeydown(self, aKey, anAction, fromObject):
        self.applicationContext.inputObserver.addKeydownObserver(fromObject, aKey, self.device, anAction)

    def mapKeyup(self, aKey, anAction, fromObject):
        self.applicationContext.inputObserver.addKeyupObserver(fromObject, aKey, self.device, anAction)

    def unmap(self):
        self.applicationContext.inputObserver.removeFrom(self.component)
        self.applicationContext.inputObserver.removeFrom(self)

    def draw(self, anArea):
        self.component.draw(anArea)

    def update(self, millisecondsSinceLastUpdate):
        self.component.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.unmap()

    def mapUserSelectComponent(self, aUserSelectComponent):
        if self.device == 100:
            self.mapKeydown(pygame.K_UP, aUserSelectComponent.startMovingUp, aUserSelectComponent)
            self.mapKeydown(pygame.K_w, aUserSelectComponent.startMovingUp, aUserSelectComponent)
            self.mapKeydown(pygame.K_DOWN, aUserSelectComponent.startMovingDown, aUserSelectComponent)
            self.mapKeydown(pygame.K_s, aUserSelectComponent.startMovingDown, aUserSelectComponent)
            self.mapKeydown(pygame.K_LEFT, aUserSelectComponent.startMovingLeft, aUserSelectComponent)
            self.mapKeydown(pygame.K_a, aUserSelectComponent.startMovingLeft, aUserSelectComponent)
            self.mapKeydown(pygame.K_RIGHT, aUserSelectComponent.startMovingRight, aUserSelectComponent)
            self.mapKeydown(pygame.K_d, aUserSelectComponent.startMovingRight, aUserSelectComponent)

            self.mapKeyup(pygame.K_UP, aUserSelectComponent.stopMovingUp, aUserSelectComponent)
            self.mapKeyup(pygame.K_w, aUserSelectComponent.stopMovingUp, aUserSelectComponent)
            self.mapKeyup(pygame.K_DOWN, aUserSelectComponent.stopMovingDown, aUserSelectComponent)
            self.mapKeyup(pygame.K_s, aUserSelectComponent.stopMovingDown, aUserSelectComponent)
            self.mapKeyup(pygame.K_LEFT, aUserSelectComponent.stopMovingLeft, aUserSelectComponent)
            self.mapKeyup(pygame.K_a, aUserSelectComponent.stopMovingLeft, aUserSelectComponent)
            self.mapKeyup(pygame.K_RIGHT, aUserSelectComponent.stopMovingRight, aUserSelectComponent)
            self.mapKeyup(pygame.K_d, aUserSelectComponent.stopMovingRight, aUserSelectComponent)

            self.mapKeydown(pygame.K_RETURN, aUserSelectComponent.accept, aUserSelectComponent)
            self.mapKeydown(pygame.K_SPACE, aUserSelectComponent.accept, aUserSelectComponent)
            self.mapKeydown(pygame.K_ESCAPE, aUserSelectComponent.exit, aUserSelectComponent)

    def mapGameComponent(self, aGameComponent):
        if self.device == 100:
            self.mapKeydown(pygame.K_LEFT, aGameComponent.startMovingLeft, aGameComponent)
            self.mapKeyup(pygame.K_LEFT, aGameComponent.stopMovingLeft, aGameComponent)
            self.mapKeydown(pygame.K_RIGHT, aGameComponent.startMovingRight, aGameComponent)
            self.mapKeyup(pygame.K_RIGHT, aGameComponent.stopMovingRight, aGameComponent)
            self.mapKeydown(pygame.K_s, aGameComponent.startDropping, aGameComponent)
            self.mapKeyup(pygame.K_s, aGameComponent.stopDropping, aGameComponent)
            self.mapKeydown(pygame.K_w, aGameComponent.hardDrop, aGameComponent)
            self.mapKeydown(pygame.K_SPACE, aGameComponent.hardDrop, aGameComponent)
            self.mapKeydown(pygame.K_a, aGameComponent.rotateLeft, aGameComponent)
            self.mapKeydown(pygame.K_d, aGameComponent.rotateRight, aGameComponent)
            self.mapKeydown(pygame.K_DOWN, aGameComponent.rotateLeft, aGameComponent)
            self.mapKeydown(pygame.K_UP, aGameComponent.rotateRight, aGameComponent)
            self.mapKeydown(pygame.K_LSHIFT, aGameComponent.hold, aGameComponent)
            self.mapKeydown(pygame.K_ESCAPE, aGameComponent.togglePause, aGameComponent)
            self.mapKeydown(pygame.K_RETURN, aGameComponent.pauseAccept, aGameComponent)
        else:
            self.mapKeydown("JOYSTICK_LEFT_STICK_LEFT", aGameComponent.startMovingLeft, aGameComponent)
            self.mapKeyup("JOYSTICK_LEFT_STICK_LEFT", aGameComponent.stopMovingLeft, aGameComponent)
            self.mapKeydown("JOYSTICK_LEFT_TRIGGER", aGameComponent.startMovingLeft, aGameComponent)
            self.mapKeyup("JOYSTICK_LEFT_TRIGGER", aGameComponent.stopMovingLeft, aGameComponent)
            self.mapKeydown("JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.startMovingRight, aGameComponent)
            self.mapKeyup("JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.stopMovingRight, aGameComponent)
            self.mapKeydown("JOYSTICK_RIGHT_TRIGGER", aGameComponent.startMovingRight, aGameComponent)
            self.mapKeyup("JOYSTICK_RIGHT_TRIGGER", aGameComponent.stopMovingRight, aGameComponent)
            self.mapKeydown("JOYSTICK_LEFT_STICK_DOWN", aGameComponent.startDropping, aGameComponent)
            self.mapKeyup("JOYSTICK_LEFT_STICK_DOWN", aGameComponent.stopDropping, aGameComponent)
            self.mapKeydown("JOYSTICK_LEFT_STICK_UP", aGameComponent.hardDrop, aGameComponent)
            self.mapKeydown("JOYSTICK_HAT_LEFT", aGameComponent.startMovingLeft, aGameComponent)
            self.mapKeyup("JOYSTICK_HAT_LEFT", aGameComponent.stopMovingLeft, aGameComponent)
            self.mapKeydown("JOYSTICK_HAT_RIGHT", aGameComponent.startMovingRight, aGameComponent)
            self.mapKeyup("JOYSTICK_HAT_RIGHT", aGameComponent.stopMovingRight, aGameComponent)
            self.mapKeydown("JOYSTICK_HAT_DOWN", aGameComponent.startDropping, aGameComponent)
            self.mapKeyup("JOYSTICK_HAT_DOWN", aGameComponent.stopDropping, aGameComponent)
            self.mapKeydown("JOYSTICK_HAT_UP", aGameComponent.hardDrop, aGameComponent)
            self.mapKeydown("JOYSTICK_RIGHT_STICK_LEFT", aGameComponent.rotateLeft, aGameComponent)
            self.mapKeydown("JOYSTICK_RIGHT_STICK_RIGHT", aGameComponent.rotateRight, aGameComponent)
            self.mapKeydown("JOYSTICK_RIGHT_STICK_UP", aGameComponent.hold, aGameComponent)
            self.mapKeydown("JOYSTICK_LEFT_BUMPER", aGameComponent.rotateLeft, aGameComponent)
            self.mapKeydown("JOYSTICK_RIGHT_BUMPER", aGameComponent.rotateRight, aGameComponent)
            self.mapKeydown("JOYSTICK_PAUSE", aGameComponent.togglePause, aGameComponent)
            self.mapKeydown("JOYSTICK_TRIANGLE", self.restartGame, aGameComponent)
            self.mapKeydown("JOYSTICK_CROSS", aGameComponent.pauseAccept, aGameComponent)


class DeviceComponents:
    def __init__(self, anApplicationContext):
        self.applicationContext = anApplicationContext
        self.components = {}

        self.applicationContext.inputObserver.addKeydownObserver(self, pygame.K_SPACE, 100, lambda: self.addDeviceIfNotIncluded(100))

        self.applicationContext.joystickLifecycleObserver.onJoystickConnected(
            lambda joystick: self.applicationContext.inputObserver.addKeydownObserver(
                self,
                "JOYSTICK_CROSS",
                joystick.get_instance_id(),
                lambda: self.addDeviceIfNotIncluded(joystick.get_instance_id())
            )
        )
        self.applicationContext.joystickLifecycleObserver.onJoystickDisconnected(lambda device: self.removeDevice(device))

    def includesDevice(self, aDevice):
        return aDevice in self.components.keys()

    def removeDevice(self, aDevice):
        if self.includesDevice(aDevice):
            self.components[aDevice].destroy()
            del self.components[aDevice]

    def addDevice(self, aDevice):
        self.components[aDevice] = DeviceComponent(
            self.applicationContext,
            aDevice,
            lambda: self.removeDevice(aDevice)
        )

    def addDeviceIfNotIncluded(self, aDevice):
        if not self.includesDevice(aDevice):
            self.addDevice(aDevice)

    def values(self) -> list[DeviceComponent]:
        values = []
        for key in self.components.keys():
            values.append(self.components[key])
        return values

    def sortedValues(self) -> list[DeviceComponent]:
        keys = []
        for key in self.components.keys():
            keys.append(key)
        keys.sort()
        values = []
        for key in keys:
            values.append(self.components[key])
        return values


class MultipleDevicePlayComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self.initializeAllGames()

    def initializeAllGames(self):
        self.destroy()
        self.rows = 20
        self.cols = 10
        self.cellSize = 25

        self.components = DeviceComponents(self.applicationContext)

    def destroy(self):
        self.applicationContext.inputObserver.removeFrom(self)

    def draw(self, anArea):
        sortedComoponents = self.components.sortedValues()
        if len(sortedComoponents) == 0:
            self.applicationContext.drawText("TETRIS", (255, 255, 255), 60, Area(0, 0, 125, 20).centeredAt(anArea).shifted(0, -50))
            self.applicationContext.drawText("Press space or X to start!", (255, 255, 255), 40, Area(0, 0, 450, 20).centeredAt(anArea).shifted(0, 20))
        if len(sortedComoponents) == 1:
            sortedComoponents[0].draw(anArea)
        if len(sortedComoponents) == 2:
            leftArea = anArea.copy()
            leftArea.width /= 2
            rightArea = leftArea.copy()
            rightArea.x = rightArea.width

            sortedComoponents[0].draw(leftArea)
            sortedComoponents[1].draw(rightArea)
        if len(sortedComoponents) == 3:
            leftArea = anArea.copy()
            leftArea.width /= 3
            middleArea = leftArea.copy()
            middleArea.x = leftArea.width
            rightArea = leftArea.copy()
            rightArea.x = rightArea.width * 2

            sortedComoponents[0].draw(leftArea)
            sortedComoponents[1].draw(middleArea)
            sortedComoponents[2].draw(rightArea)
        if len(sortedComoponents) == 4:
            topLeftArea = anArea.copy()
            topLeftArea.width /= 2
            topLeftArea.height /= 2
            topRightArea = topLeftArea.copy()
            topRightArea.x = topRightArea.width
            bottomLeftArea = topLeftArea.copy()
            bottomLeftArea.y = topLeftArea.height
            bottomRightArea = topLeftArea.copy()
            bottomRightArea.x = topRightArea.width
            bottomRightArea.y = topLeftArea.height

            sortedComoponents[0].draw(topLeftArea)
            sortedComoponents[1].draw(topRightArea)
            sortedComoponents[2].draw(bottomLeftArea)
            sortedComoponents[3].draw(bottomRightArea)

    def update(self, millisecondsSinceLastUpdate):
        for gameComponent in self.components.values():
            gameComponent.update(millisecondsSinceLastUpdate)
