from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
from desktop.input_observer import InputObserver
from desktop.application_context import ApplicationContext
from desktop.play_page_component import PlayPageComponent
from desktop.area import Area
import pygame


class JoystickLifecycleObserver:
    def __init__(self):
        self.joystickCreationObservers = []

    def onJoystickCreation(self, anObserver):
        self.joystickCreationObservers.append(anObserver)

    def joystickWasCreated(self, aController):
        for observer in self.joystickCreationObservers:
            observer(aController)


class JoystickAxisHandler:
    def __init__(self, aJoystick, anApplicationContext):
        self.joystick = aJoystick
        self.applicationContext = anApplicationContext
        self.joystickLeftStickLeft = False
        self.joystickLeftStickRight = False
        self.joystickLeftStickUp = False
        self.joystickLeftStickDown = False
        self.joystickRightStickLeft = False
        self.joystickRightStickRight = False

    def handleAxisMovement(self):
        joystickId = self.joystick.get_instance_id()
        if self.joystick.get_axis(0) < -0.5 and not self.joystickLeftStickLeft:
            self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_LEFT", joystickId)
            self.joystickLeftStickLeft = True
        if self.joystick.get_axis(0) >= -0.5 and self.joystickLeftStickLeft:
            self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_LEFT", joystickId)
            self.joystickLeftStickLeft = False

        if self.joystick.get_axis(0) >= 0.5 and not self.joystickLeftStickRight:
            self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_RIGHT", joystickId)
            self.joystickLeftStickRight = True
        if self.joystick.get_axis(0) < 0.5 and self.joystickLeftStickRight:
            self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_RIGHT", joystickId)
            self.joystickLeftStickRight = False

        if self.joystick.get_axis(1) < -0.85 and not self.joystickLeftStickUp:
            self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_UP", joystickId)
            self.joystickLeftStickUp = True
        if self.joystick.get_axis(1) >= -0.5 and self.joystickLeftStickUp:
            self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_UP", joystickId)
            self.joystickLeftStickUp = False

        if self.joystick.get_axis(1) >= 0.5 and not self.joystickLeftStickDown:
            self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_DOWN", joystickId)
            self.joystickLeftStickDown = True
        if self.joystick.get_axis(1) < 0.5 and self.joystickLeftStickDown:
            self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_DOWN", joystickId)
            self.joystickLeftStickDown = False

        if self.joystick.get_axis(3) < -0.5 and not self.joystickRightStickLeft:
            self.applicationContext.inputObserver.keydown("JOYSTICK_RIGHT_STICK_LEFT", joystickId)
            self.joystickRightStickLeft = True
        if self.joystick.get_axis(3) >= -0.5 and self.joystickRightStickLeft:
            self.applicationContext.inputObserver.keyup("JOYSTICK_RIGHT_STICK_LEFT", joystickId)
            self.joystickRightStickLeft = False

        if self.joystick.get_axis(3) >= 0.5 and not self.joystickRightStickRight:
            self.applicationContext.inputObserver.keydown("JOYSTICK_RIGHT_STICK_RIGHT", joystickId)
            self.joystickRightStickRight = True
        if self.joystick.get_axis(3) < 0.5 and self.joystickRightStickRight:
            self.applicationContext.inputObserver.keyup("JOYSTICK_RIGHT_STICK_RIGHT", joystickId)
            self.joystickRightStickRight = False


class DesktopApplicationRunner:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.joystick.init()
        self.joysticks = {}
        self.clock = pygame.time.Clock()
        self.joystickLifecycleObserver = JoystickLifecycleObserver()
        self.applicationContext = ApplicationContext(
            pygame.display.set_mode((1280,720)),
            InputObserver(),
            self.createFont(),
            self.joysticks,
            self.joystickLifecycleObserver
        )
        self.page = PlayPageComponent(self.applicationContext)
        self.timeSinceLastFrame = 0
        self.joystickAxisHandlers = {}
        self.applicationContext.joystickLifecycleObserver.onJoystickCreation(self.addJoystickAxisHandler)

    def addJoystickAxisHandler(self, aJoystickId):
        self.joystickAxisHandlers[aJoystickId] = JoystickAxisHandler(aJoystickId, self.applicationContext)

    def createFont(self):
        font_file = pygame.font.get_default_font()
        return pygame.font.Font(font_file, 20)

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                self.applicationContext.inputObserver.keydown(event.key, 0)
            if event.type == pygame.KEYUP:
                self.applicationContext.inputObserver.keyup(event.key, 0)
            if event.type == pygame.JOYBUTTONDOWN:
                print(event.button)
                self.applicationContext.inputObserver.keydown(event.button, event.instance_id)
            if event.type == pygame.JOYBUTTONUP:
                self.applicationContext.inputObserver.keyup(event.button, event.instance_id)
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                self.joystickLifecycleObserver.joystickWasCreated(joy)
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        for joystickAxisHandler in self.joystickAxisHandlers.values():
            joystickAxisHandler.handleAxisMovement()

    def drawScreen(self):
        self.applicationContext.screen.fill("black")
        self.page.draw(Area(0, 0, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))

    def drawRect(self, aColor, aRectangle):
        pygame.draw.rect(self.applicationContext.screen, aColor, aRectangle)

    def update(self):
        self.page.update(self.timeSinceLastFrame)

    def run(self):
        while True:
            self.eventHandler()
            self.drawScreen()
            self.update()

            pygame.display.flip()
            self.timeSinceLastFrame = self.clock.tick(60)
