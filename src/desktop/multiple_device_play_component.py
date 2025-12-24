from pygame.joystick import Joystick
from desktop.desktop_component import DesktopComponent
from desktop.area import Area
from desktop.color_scheme import ColorScheme
from tetris_model.tetris_event_notifier import TetrisEventNotifier
from tetris_model.tetris_game import TetrisGame
from tetris_model.rotation_list_generator import NintendoRotationListGenerator, SegaRotationListGenerator, SuperRotationListGenerator
from tetris_model.kicks import SRSKicks
from tetris_model.rand import Rand
from desktop.game_component import GameComponent
import pygame


class DeviceComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aDevice, aDeletionFunction):
        self.applicationContext = anApplicationContext
        self.device = aDevice
        self.deletionFunction = aDeletionFunction
        self.rows = 20
        self.cols = 10
        self.cellSize = 25
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
            self.deleteGame
        )

    def deleteGame(self):
        self.deletionFunction()

    def restartGame(self):
        self.unmap()
        self.gameComponent = self.createGameComponent()

    def mapKeydown(self, aKey, anAction):
        self.applicationContext.inputObserver.addKeydownObserver(self, aKey, self.device, anAction)

    def mapKeyup(self, aKey, anAction):
        self.applicationContext.inputObserver.addKeyupObserver(self, aKey, self.device, anAction)

    def unmap(self):
        self.applicationContext.inputObserver.removeFrom(self)

    def draw(self, anArea):
        self.component.draw(anArea)

    def update(self, millisecondsSinceLastUpdate):
        self.component.update(millisecondsSinceLastUpdate)

    def destroy(self):
        self.unmap()

    def mapGameComponent(self, aGameComponent):
        if self.device == 100:
            self.mapKeydown(pygame.K_LEFT, aGameComponent.startMovingLeft)
            self.mapKeyup(pygame.K_LEFT, aGameComponent.stopMovingLeft)
            self.mapKeydown(pygame.K_RIGHT, aGameComponent.startMovingRight)
            self.mapKeyup(pygame.K_RIGHT, aGameComponent.stopMovingRight)
            self.mapKeydown(pygame.K_s, aGameComponent.startDropping)
            self.mapKeyup(pygame.K_s, aGameComponent.stopDropping)
            self.mapKeydown(pygame.K_w, aGameComponent.hardDrop)
            self.mapKeydown(pygame.K_SPACE, aGameComponent.hardDrop)
            self.mapKeydown(pygame.K_a, aGameComponent.rotateLeft)
            self.mapKeydown(pygame.K_d, aGameComponent.rotateRight)
            self.mapKeydown(pygame.K_DOWN, aGameComponent.rotateLeft)
            self.mapKeydown(pygame.K_UP, aGameComponent.rotateRight)
            self.mapKeydown(pygame.K_LSHIFT, aGameComponent.hold)
            self.mapKeydown(pygame.K_ESCAPE, aGameComponent.togglePause)
            self.mapKeydown(pygame.K_RETURN, aGameComponent.pauseAccept)
        else:
            self.mapKeydown("JOYSTICK_LEFT_STICK_LEFT", aGameComponent.startMovingLeft)
            self.mapKeyup("JOYSTICK_LEFT_STICK_LEFT", aGameComponent.stopMovingLeft)
            self.mapKeydown("JOYSTICK_LEFT_TRIGGER", aGameComponent.startMovingLeft)
            self.mapKeyup("JOYSTICK_LEFT_TRIGGER", aGameComponent.stopMovingLeft)
            self.mapKeydown("JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.startMovingRight)
            self.mapKeyup("JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.stopMovingRight)
            self.mapKeydown("JOYSTICK_RIGHT_TRIGGER", aGameComponent.startMovingRight)
            self.mapKeyup("JOYSTICK_RIGHT_TRIGGER", aGameComponent.stopMovingRight)
            self.mapKeydown("JOYSTICK_LEFT_STICK_DOWN", aGameComponent.startDropping)
            self.mapKeyup("JOYSTICK_LEFT_STICK_DOWN", aGameComponent.stopDropping)
            self.mapKeydown("JOYSTICK_LEFT_STICK_UP", aGameComponent.hardDrop)
            self.mapKeydown("JOYSTICK_HAT_LEFT", aGameComponent.startMovingLeft)
            self.mapKeyup("JOYSTICK_HAT_LEFT", aGameComponent.stopMovingLeft)
            self.mapKeydown("JOYSTICK_HAT_RIGHT", aGameComponent.startMovingRight)
            self.mapKeyup("JOYSTICK_HAT_RIGHT", aGameComponent.stopMovingRight)
            self.mapKeydown("JOYSTICK_HAT_DOWN", aGameComponent.startDropping)
            self.mapKeyup("JOYSTICK_HAT_DOWN", aGameComponent.stopDropping)
            self.mapKeydown("JOYSTICK_HAT_UP", aGameComponent.hardDrop)
            self.mapKeydown("JOYSTICK_RIGHT_STICK_LEFT", aGameComponent.rotateLeft)
            self.mapKeydown("JOYSTICK_RIGHT_STICK_RIGHT", aGameComponent.rotateRight)
            self.mapKeydown("JOYSTICK_RIGHT_STICK_UP", aGameComponent.hold)
            self.mapKeydown("JOYSTICK_LEFT_BUMPER", aGameComponent.rotateLeft)
            self.mapKeydown("JOYSTICK_RIGHT_BUMPER", aGameComponent.rotateRight)
            self.mapKeydown("JOYSTICK_PAUSE", aGameComponent.togglePause)
            self.mapKeydown("JOYSTICK_TRIANGLE", self.restartGame)
            self.mapKeydown("JOYSTICK_CROSS", aGameComponent.pauseAccept)


class DeviceComponents:
    def __init__(self, anApplicationContext):
        self.applicationContext = anApplicationContext
        self.components = {}

        self.applicationContext.inputObserver.addKeydownObserver(self, pygame.K_SPACE, 100, lambda: self.addDevice(100))

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
