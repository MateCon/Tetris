from desktop.input_observer import InputObserver
from desktop.application_context import ApplicationContext
from desktop.play_page_component import PlayPageComponent
from desktop.area import Area
from desktop.joystick_observer import JoystickObserver, JoystickLifecycleObserver
import pygame


class DesktopApplicationRunner:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        pygame.display.set_icon(pygame.image.load("assets/images/logo.png"))
        pygame.font.init()
        pygame.joystick.init()
        self.joysticks = {}
        self.clock = pygame.time.Clock()
        self.joystickLifecycleObserver = JoystickLifecycleObserver()
        self.applicationContext = ApplicationContext(
            pygame.display.set_mode(),
            InputObserver(),
            self.joysticks,
            self.joystickLifecycleObserver
        )
        self.page = PlayPageComponent(self.applicationContext)
        self.timeSinceLastFrame = 0
        self.joystickObservers = {}
        self.applicationContext.joystickLifecycleObserver.onJoystickConnected(self.addJoystickObserver)

    def addJoystickObserver(self, aJoystickId):
        self.joystickObservers[aJoystickId] = JoystickObserver(aJoystickId, self.applicationContext)

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                self.applicationContext.inputObserver.keydown(event.key, 100)
            if event.type == pygame.KEYUP:
                self.applicationContext.inputObserver.keyup(event.key, 100)
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                self.joystickLifecycleObserver.joystickConnected(joy)
            if event.type == pygame.JOYDEVICEREMOVED:
                self.joystickLifecycleObserver.joystickDisconnected(event.instance_id)
                del self.joysticks[event.instance_id]

        for joystickObserver in self.joystickObservers.values():
            joystickObserver.update()

    def drawScreen(self):
        self.applicationContext.screen.fill("black")
        self.page.draw(Area(0, 0, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))

    def update(self):
        self.page.update(self.timeSinceLastFrame)

    def run(self):
        while self.applicationContext.isRunning:
            self.eventHandler()
            self.drawScreen()
            self.update()

            pygame.display.flip()
            self.timeSinceLastFrame = self.clock.tick(30)
