from pygame.joystick import Joystick
from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
from desktop.area import Area
from model.tetris_event_notifier import TetrisEventNotifier
from model.tetris_game import TetrisGame
from model.rotation_list_generator import SuperRotationListGenerator
from model.kicks import ARSKicks
from model.rand import Rand
import pygame


class ColorScheme:
    def __init__(self):
        self.colors = {
            'i': pygame.Color(255, 0, 0),
            'j': pygame.Color(0, 0, 255),
            'l': pygame.Color(255, 172, 0),
            'o': pygame.Color(255, 255, 0),
            's': pygame.Color(0, 255, 255),
            't': pygame.Color(255, 0, 255),
            'z': pygame.Color(0, 255, 0),
        }

    def cellColor(self, aChar, isPaused, currentPiece):
        isGhost = False

        if aChar == '#':
            aChar = currentPiece
            isGhost = True

        if aChar in self.colors.keys():
            color = self.colors[aChar]
            if isGhost:
                color = pygame.Color(color.r // 5, color.g // 5, color.b // 5)
            if isPaused:
                return color.grayscale()
            return color
        return pygame.Color(0, 0, 0)


class PlayPageComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self.initializeAllGames()

    def initializeAllGames(self):
        self.destroy()
        self.rows = 20
        self.cols = 10
        self.cellSize = 25

        self.gameComponents = {}

        self.applicationContext.inputObserver.addKeydownObserver(self, pygame.K_SPACE, 100, self.createGameComponentWithKeyboard)

        self.applicationContext.joystickLifecycleObserver.onJoystickConnected(lambda joystick: self.mapCreateGame(joystick.get_instance_id()))
        self.applicationContext.joystickLifecycleObserver.onJoystickDisconnected(self.deleteGameComponentWithJoystickId)
        self.applicationContext.joystickLifecycleObserver.onJoystickDisconnected(self.unmapCreateGame)

    def mapCreateGame(self, anInstanceId):
        self.applicationContext.inputObserver.removeDevice(anInstanceId)
        self.applicationContext.inputObserver.addKeydownObserver(self, "JOYSTICK_CROSS", anInstanceId, lambda: self.createGameComponentWithJoystickId(anInstanceId))

    def unmapCreateGame(self, anInstanceId):
        self.applicationContext.inputObserver.removePair(anInstanceId, "JOYSTICK_CROSS")

    def destroy(self):
        self.applicationContext.inputObserver.removeFrom(self)

    def createGameComponentWithKeyboard(self):
        if not 100 in self.gameComponents.keys():
            self.createGameComponent(100, self.mapKeyboard)

    def deleteGameComponentWithKeyboard(self):
        if 100 in self.gameComponents.keys():
            self.gameComponents[100].destroy()
            del self.gameComponents[100]

    def createGameComponentWithJoystickId(self, anInstanceId):
        self.createGameComponent(anInstanceId, self.createJoystickMapper(anInstanceId))

    def createGameComponentWithJoystick(self, aJoystick):
        self.createGameComponentWithJoystickId(aJoystick.get_instance_id())

    def deleteGameComponentWithJoystickId(self, anInstanceId):
        if anInstanceId in self.gameComponents.keys():
            self.gameComponents[anInstanceId].destroy()
            del self.gameComponents[anInstanceId]
            self.mapCreateGame(anInstanceId)

    def createGameComponent(self, anInstanceId, aKeybindMapper):
        tetrisEventNotifier = TetrisEventNotifier()
        game = TetrisGame(
            self.cols,
            self.rows,
            Rand(),
            SuperRotationListGenerator,
            ARSKicks,
            tetrisEventNotifier
        )

        gameComponent = TetrisGameComponent(
            self.applicationContext,
            game,
            self.rows,
            self.cols,
            self.cellSize,
            tetrisEventNotifier,
            aKeybindMapper,
            ColorScheme(),
            lambda: self.restartGame(anInstanceId),
            lambda: self.deleteGame(anInstanceId)
        )
        if not anInstanceId in self.gameComponents.keys():
            self.gameComponents[anInstanceId] = gameComponent

    def mapKeyboard(self, aGameComponent):
        aGameComponent.mapKeydown(100, pygame.K_LEFT, aGameComponent.startMovingLeft)
        aGameComponent.mapKeyup(100, pygame.K_LEFT, aGameComponent.stopMovingLeft)
        aGameComponent.mapKeydown(100, pygame.K_RIGHT, aGameComponent.startMovingRight)
        aGameComponent.mapKeyup(100, pygame.K_RIGHT, aGameComponent.stopMovingRight)
        aGameComponent.mapKeydown(100, pygame.K_s, aGameComponent.startDropping)
        aGameComponent.mapKeyup(100, pygame.K_s, aGameComponent.stopDropping)
        aGameComponent.mapKeydown(100, pygame.K_w, aGameComponent.hardDrop)
        aGameComponent.mapKeydown(100, pygame.K_SPACE, aGameComponent.hardDrop)
        aGameComponent.mapKeydown(100, pygame.K_a, aGameComponent.rotateLeft)
        aGameComponent.mapKeydown(100, pygame.K_d, aGameComponent.rotateRight)
        aGameComponent.mapKeydown(100, pygame.K_DOWN, aGameComponent.rotateLeft)
        aGameComponent.mapKeydown(100, pygame.K_UP, aGameComponent.rotateRight)
        aGameComponent.mapKeydown(100, pygame.K_LSHIFT, aGameComponent.hold)
        aGameComponent.mapKeydown(100, pygame.K_ESCAPE, aGameComponent.togglePause)
        aGameComponent.mapKeydown(100, pygame.K_RETURN, aGameComponent.pauseAccept)

    def createJoystickMapper(self, aDeviceId):
        def mapJoystick(aGameComponent):
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_LEFT", aGameComponent.startMovingLeft)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_LEFT", aGameComponent.stopMovingLeft)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_TRIGGER", aGameComponent.startMovingLeft)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_TRIGGER", aGameComponent.stopMovingLeft)

            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.startMovingRight)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.stopMovingRight)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_RIGHT_TRIGGER", aGameComponent.startMovingRight)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_RIGHT_TRIGGER", aGameComponent.stopMovingRight)

            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_DOWN", aGameComponent.startDropping)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_DOWN", aGameComponent.stopDropping)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_UP", aGameComponent.hardDrop)

            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_HAT_LEFT", aGameComponent.startMovingLeft)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_HAT_LEFT", aGameComponent.stopMovingLeft)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_HAT_RIGHT", aGameComponent.startMovingRight)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_HAT_RIGHT", aGameComponent.stopMovingRight)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_HAT_DOWN", aGameComponent.startDropping)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_HAT_DOWN", aGameComponent.stopDropping)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_HAT_UP", aGameComponent.hardDrop)

            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_RIGHT_STICK_LEFT", aGameComponent.rotateLeft)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_RIGHT_STICK_RIGHT", aGameComponent.rotateRight)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_RIGHT_STICK_UP", aGameComponent.hold)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_BUMPER", aGameComponent.rotateLeft)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_RIGHT_BUMPER", aGameComponent.rotateRight)

            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_PAUSE", aGameComponent.togglePause)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_TRIANGLE", lambda: self.restartGame(aDeviceId))
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_CROSS", aGameComponent.pauseAccept)

        return mapJoystick

    def restartGame(self, aDeviceId):
        if aDeviceId == 100:
            self.deleteGameComponentWithKeyboard()
            self.createGameComponentWithKeyboard()
        else:
            self.deleteGameComponentWithJoystickId(aDeviceId)
            self.createGameComponentWithJoystickId(aDeviceId)

    def deleteGame(self, aDeviceId):
        if aDeviceId in self.gameComponents.keys():
            self.gameComponents[aDeviceId].destroy()
            del self.gameComponents[aDeviceId]

    def draw(self, anArea):
        keysSet = self.gameComponents.keys()
        keys = []
        for key in keysSet:
            keys.append(key)
        keys.sort()
        if len(self.gameComponents) == 0:
            self.applicationContext.drawText("TETRIS", (255, 255, 255), 60, Area(0, 0, 125, 20).centeredAt(anArea).shifted(0, -50))
            self.applicationContext.drawText("Press space or X to start!", (255, 255, 255), 40, Area(0, 0, 450, 20).centeredAt(anArea).shifted(0, 20))
        if len(self.gameComponents) == 1:
            self.gameComponents[keys[0]].draw(anArea)
        if len(self.gameComponents) == 2:
            leftArea = anArea.copy()
            leftArea.width /= 2
            rightArea = leftArea.copy()
            rightArea.x = rightArea.width

            self.gameComponents[keys[0]].draw(leftArea)
            self.gameComponents[keys[1]].draw(rightArea)
        if len(self.gameComponents) == 3:
            leftArea = anArea.copy()
            leftArea.width /= 3
            middleArea = leftArea.copy()
            middleArea.x = leftArea.width
            rightArea = leftArea.copy()
            rightArea.x = rightArea.width * 2

            self.gameComponents[keys[0]].draw(leftArea)
            self.gameComponents[keys[1]].draw(middleArea)
            self.gameComponents[keys[2]].draw(rightArea)
        if len(self.gameComponents) == 4:
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

            self.gameComponents[keys[0]].draw(topLeftArea)
            self.gameComponents[keys[1]].draw(topRightArea)
            self.gameComponents[keys[2]].draw(bottomLeftArea)
            self.gameComponents[keys[3]].draw(bottomRightArea)

    def update(self, millisecondsSinceLastUpdate):
        for gameComponent in self.gameComponents.values():
            gameComponent.update(millisecondsSinceLastUpdate)
