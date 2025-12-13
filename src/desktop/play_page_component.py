from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
from model.tetris_event_notifier import TetrisEventNotifier
from model.tetris_game import TetrisGame
from model.rotation_list_generator import NintendoRotationListGenerator
from model.kicks import ARSKicks
from model.rand import Rand
import pygame


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
            aKeybindMapper
        )
        self.gameComponents.append(gameComponent)

    def mapKeyboard(self, aGameComponent):
        aGameComponent.mapKeydown(0, pygame.K_LEFT, aGameComponent.leftCommandRepeater.start)
        aGameComponent.mapKeyup(0, pygame.K_LEFT, aGameComponent.leftCommandRepeater.stop)
        aGameComponent.mapKeydown(0, pygame.K_RIGHT, aGameComponent.rightCommandRepeater.start)
        aGameComponent.mapKeyup(0, pygame.K_RIGHT, aGameComponent.rightCommandRepeater.stop)
        aGameComponent.mapKeydown(0, pygame.K_s, aGameComponent.dropCommandRepeater.start)
        aGameComponent.mapKeyup(0, pygame.K_s, aGameComponent.dropCommandRepeater.stop)
        aGameComponent.mapKeydown(0, pygame.K_w, aGameComponent.game.hardDrop)
        aGameComponent.mapKeydown(0, pygame.K_a, aGameComponent.game.rotateLeft)
        aGameComponent.mapKeydown(0, pygame.K_d, aGameComponent.game.rotateRight)

    def createJoystickMapper(self, aDeviceId):
        def mapJoystick(aGameComponent):
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_LEFT", aGameComponent.leftCommandRepeater.start)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_LEFT", aGameComponent.leftCommandRepeater.stop)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.rightCommandRepeater.start)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_RIGHT", aGameComponent.rightCommandRepeater.stop)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_DOWN", aGameComponent.dropCommandRepeater.start)
            aGameComponent.mapKeyup(aDeviceId, "JOYSTICK_LEFT_STICK_DOWN", aGameComponent.dropCommandRepeater.stop)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_LEFT_STICK_UP", aGameComponent.game.hardDrop)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_RIGHT_STICK_LEFT", aGameComponent.game.rotateLeft)
            aGameComponent.mapKeydown(aDeviceId, "JOYSTICK_RIGHT_STICK_RIGHT", aGameComponent.game.rotateRight)

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

    def update(self, millisecondsSinceLastUpdate):
        for gameComponent in self.gameComponents:
            gameComponent.update(millisecondsSinceLastUpdate)
