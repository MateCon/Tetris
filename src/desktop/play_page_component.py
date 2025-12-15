from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
from model.tetris_event_notifier import TetrisEventNotifier
from model.tetris_game import TetrisGame
from model.rotation_list_generator import NintendoRotationListGenerator
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
        self.initializeGame()

    def initializeGame(self):
        self.destroy()
        self.rows = 20
        self.cols = 10
        self.cellSize = 25

        self.gameComponents = []

        self.createGameComponent(self.mapKeyboard)

        for joystick in self.applicationContext.joysticks.values():
            self.createGameComponentWithJoystick(joystick)

        self.applicationContext.joystickLifecycleObserver.onJoystickCreation(self.createGameComponentWithJoystick)
        self.applicationContext.inputObserver.addKeydownObserver(self, pygame.K_DELETE, 0, self.restartGame)

    def destroy(self):
        self.applicationContext.inputObserver.removeFrom(self)

    def createGameComponentWithJoystick(self, aJoystick):
        self.createGameComponent(self.createJoystickMapper(aJoystick.get_instance_id()))

    def createGameComponent(self, aKeybindMapper):
        tetrisEventNotifier = TetrisEventNotifier()
        game = TetrisGame(
            self.cols,
            self.rows,
            Rand(),
            NintendoRotationListGenerator,
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
            ColorScheme()
        )
        self.gameComponents.append(gameComponent)

    def mapKeyboard(self, aGameComponent):
        aGameComponent.mapKeydown(0, pygame.K_LEFT, aGameComponent.startMovingLeft)
        aGameComponent.mapKeyup(0, pygame.K_LEFT, aGameComponent.stopMovingLeft)
        aGameComponent.mapKeydown(0, pygame.K_RIGHT, aGameComponent.startMovingRight)
        aGameComponent.mapKeyup(0, pygame.K_RIGHT, aGameComponent.stopMovingRight)
        aGameComponent.mapKeydown(0, pygame.K_s, aGameComponent.startDropping)
        aGameComponent.mapKeyup(0, pygame.K_s, aGameComponent.stopDropping)
        aGameComponent.mapKeydown(0, pygame.K_w, aGameComponent.hardDrop)
        aGameComponent.mapKeydown(0, pygame.K_SPACE, aGameComponent.hardDrop)
        aGameComponent.mapKeydown(0, pygame.K_a, aGameComponent.rotateLeft)
        aGameComponent.mapKeydown(0, pygame.K_d, aGameComponent.rotateRight)
        aGameComponent.mapKeydown(0, pygame.K_DOWN, aGameComponent.rotateLeft)
        aGameComponent.mapKeydown(0, pygame.K_UP, aGameComponent.rotateRight)
        aGameComponent.mapKeydown(0, pygame.K_LSHIFT, aGameComponent.hold)
        aGameComponent.mapKeydown(0, pygame.K_ESCAPE, aGameComponent.togglePause)

    def createJoystickMapper(self, aDeviceId):
        def mapJoystick(aGameComponent):
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_LEFT", aGameComponent.startMovingLeft)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_LEFT", aGameComponent.stopMovingLeft)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.startMovingRight)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.stopMovingRight)
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

        return mapJoystick

    def restartGame(self):
        for gameComponent in self.gameComponents:
            gameComponent.destroy()
        self.initializeGame()

    def draw(self, anArea):
        if len(self.gameComponents) == 1:
            self.gameComponents[0].draw(anArea)
        if len(self.gameComponents) == 2:
            leftArea = anArea.copy()
            leftArea.width /= 2
            rightArea = leftArea.copy()
            rightArea.x = rightArea.width

            self.gameComponents[0].draw(leftArea)
            self.gameComponents[1].draw(rightArea)
        if len(self.gameComponents) == 3:
            leftArea = anArea.copy()
            leftArea.width /= 3
            middleArea = leftArea.copy()
            middleArea.x = leftArea.width
            rightArea = leftArea.copy()
            rightArea.x = rightArea.width * 2

            self.gameComponents[0].draw(leftArea)
            self.gameComponents[1].draw(middleArea)
            self.gameComponents[2].draw(rightArea)
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

            self.gameComponents[0].draw(topLeftArea)
            self.gameComponents[1].draw(topRightArea)
            self.gameComponents[2].draw(bottomLeftArea)
            self.gameComponents[3].draw(bottomRightArea)

    def update(self, millisecondsSinceLastUpdate):
        for gameComponent in self.gameComponents:
            gameComponent.update(millisecondsSinceLastUpdate)
