from desktop.desktop_component import DesktopComponent
from desktop.area import Area
from desktop.color_scheme import ColorScheme
from tetris_model.tetris_event_notifier import TetrisEventNotifier
from tetris_model.tetris_game import TetrisGame
from tetris_model.rotation_list_generator import SuperRotationListGenerator
from tetris_model.kicks import SRSKicks
from tetris_model.rand import Rand
from desktop.game_component import GameComponent
from desktop.user_select import UserSelectComponent
import pygame


class DeviceComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aDevice, aDeletionFunction):
        self.applicationContext = anApplicationContext
        self.device = aDevice
        self.deletionFunction = aDeletionFunction
        self.rows = 20
        self.cols = 10
        self.cellSize = 25
        self.component = self.createUserSelectComponent()
        self.session = None

    def createUserSelectComponent(self):
        return UserSelectComponent(
            self.applicationContext,
            self.rows,
            self.cols,
            self.cellSize,
            self.mapForm,
            self.playWith,
            self.deletionFunction
        )

    def playWith(self, aSession):
        self.session = aSession
        self.applicationContext.savedSessions.using(self.session)
        self.component.destroy()
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
            self.deletionFunction,
            self.session,
            self.mapForm
        )

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
        if self.session is not None:
            self.applicationContext.savedSessions.stopUsing(self.session)

    def mapForm(self, aForm):
        if self.device == 100:
            self.mapKeydown(pygame.K_UP, aForm.startMovingUp, aForm)
            self.mapKeydown(pygame.K_w, aForm.startMovingUp, aForm)
            self.mapKeydown(pygame.K_DOWN, aForm.startMovingDown, aForm)
            self.mapKeydown(pygame.K_s, aForm.startMovingDown, aForm)
            self.mapKeydown(pygame.K_LEFT, aForm.startMovingLeft, aForm)
            self.mapKeydown(pygame.K_a, aForm.startMovingLeft, aForm)
            self.mapKeydown(pygame.K_RIGHT, aForm.startMovingRight, aForm)
            self.mapKeydown(pygame.K_d, aForm.startMovingRight, aForm)

            self.mapKeyup(pygame.K_UP, aForm.stopMovingUp, aForm)
            self.mapKeyup(pygame.K_w, aForm.stopMovingUp, aForm)
            self.mapKeyup(pygame.K_DOWN, aForm.stopMovingDown, aForm)
            self.mapKeyup(pygame.K_s, aForm.stopMovingDown, aForm)
            self.mapKeyup(pygame.K_LEFT, aForm.stopMovingLeft, aForm)
            self.mapKeyup(pygame.K_a, aForm.stopMovingLeft, aForm)
            self.mapKeyup(pygame.K_RIGHT, aForm.stopMovingRight, aForm)
            self.mapKeyup(pygame.K_d, aForm.stopMovingRight, aForm)

            self.mapKeydown(pygame.K_RETURN, aForm.accept, aForm)
            self.mapKeydown(pygame.K_SPACE, aForm.accept, aForm)
            self.mapKeydown(pygame.K_ESCAPE, aForm.exit, aForm)
        else:
            self.mapKeydown("JOYSTICK_LEFT_STICK_UP", aForm.startMovingUp, aForm)
            self.mapKeydown("JOYSTICK_HAT_UP", aForm.startMovingUp, aForm)
            self.mapKeydown("JOYSTICK_LEFT_STICK_DOWN", aForm.startMovingDown, aForm)
            self.mapKeydown("JOYSTICK_HAT_DOWN", aForm.startMovingDown, aForm)
            self.mapKeydown("JOYSTICK_LEFT_STICK_LEFT", aForm.startMovingLeft, aForm)
            self.mapKeydown("JOYSTICK_HAT_LEFT", aForm.startMovingLeft, aForm)
            self.mapKeydown("JOYSTICK_LEFT_STICK_RIGHT", aForm.startMovingRight, aForm)
            self.mapKeydown("JOYSTICK_HAT_RIGHT", aForm.startMovingRight, aForm)

            self.mapKeyup("JOYSTICK_LEFT_STICK_UP", aForm.stopMovingUp, aForm)
            self.mapKeyup("JOYSTICK_HAT_UP", aForm.stopMovingUp, aForm)
            self.mapKeyup("JOYSTICK_LEFT_STICK_DOWN", aForm.stopMovingDown, aForm)
            self.mapKeyup("JOYSTICK_HAT_DOWN", aForm.stopMovingDown, aForm)
            self.mapKeyup("JOYSTICK_LEFT_STICK_LEFT", aForm.stopMovingLeft, aForm)
            self.mapKeyup("JOYSTICK_HAT_LEFT", aForm.stopMovingLeft, aForm)
            self.mapKeyup("JOYSTICK_LEFT_STICK_RIGHT", aForm.stopMovingRight, aForm)
            self.mapKeyup("JOYSTICK_HAT_RIGHT", aForm.stopMovingRight, aForm)

            self.mapKeydown("JOYSTICK_CROSS", aForm.accept, aForm)
            self.mapKeydown("JOYSTICK_RIGHT_BUMPER", aForm.accept, aForm)
            self.mapKeydown("JOYSTICK_CIRCLE", aForm.exit, aForm)

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
