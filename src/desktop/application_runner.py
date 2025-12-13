from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
from desktop.input_observer import InputObserver
from desktop.application_context import ApplicationContext
from desktop.play_page_component import PlayPageComponent
from desktop.area import Area
import pygame


class DesktopApplicationRunner:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.joystick.init()
        self.joysticks = {}
        self.clock = pygame.time.Clock()
        self.applicationContext = ApplicationContext(
            pygame.display.set_mode((1280,720)),
            InputObserver(),
            self.createFont()
        )
        self.page = PlayPageComponent(self.applicationContext)
        self.timeSinceLastFrame = 0

        self.joystickLeftStickLeft = False
        self.joystickLeftStickRight = False
        self.joystickLeftStickUp = False
        self.joystickLeftStickDown = False
        self.joystickRightStickLeft = False
        self.joystickRightStickRight = False

    def createFont(self):
        font_file = pygame.font.get_default_font()
        return pygame.font.Font(font_file, 20)

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                self.applicationContext.inputObserver.keydown(event.key)
            if event.type == pygame.KEYUP:
                self.applicationContext.inputObserver.keyup(event.key)
            if event.type == pygame.JOYBUTTONDOWN:
                print(event.button)
                self.applicationContext.inputObserver.keydown(event.button)
            if event.type == pygame.JOYBUTTONUP:
                self.applicationContext.inputObserver.keyup(event.button)
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        for joystick in self.joysticks.values():
            if joystick.get_axis(0) < -0.5 and not self.joystickLeftStickLeft:
                self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_LEFT")
                self.joystickLeftStickLeft = True
            if joystick.get_axis(0) >= -0.5 and self.joystickLeftStickLeft:
                self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_LEFT")
                self.joystickLeftStickLeft = False

            if joystick.get_axis(0) >= 0.5 and not self.joystickLeftStickRight:
                self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_RIGHT")
                self.joystickLeftStickRight = True
            if joystick.get_axis(0) < 0.5 and self.joystickLeftStickRight:
                self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_RIGHT")
                self.joystickLeftStickRight = False

            if joystick.get_axis(1) < -0.85 and not self.joystickLeftStickUp:
                self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_UP")
                self.joystickLeftStickUp = True
            if joystick.get_axis(1) >= -0.5 and self.joystickLeftStickUp:
                self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_UP")
                self.joystickLeftStickUp = False

            if joystick.get_axis(1) >= 0.5 and not self.joystickLeftStickDown:
                self.applicationContext.inputObserver.keydown("JOYSTICK_LEFT_STICK_DOWN")
                self.joystickLeftStickDown = True
            if joystick.get_axis(1) < 0.5 and self.joystickLeftStickDown:
                self.applicationContext.inputObserver.keyup("JOYSTICK_LEFT_STICK_DOWN")
                self.joystickLeftStickDown = False

            if joystick.get_axis(3) < -0.5 and not self.joystickRightStickLeft:
                self.applicationContext.inputObserver.keydown("JOYSTICK_RIGHT_STICK_LEFT")
                self.joystickRightStickLeft = True
            if joystick.get_axis(3) >= -0.5 and self.joystickRightStickLeft:
                self.applicationContext.inputObserver.keyup("JOYSTICK_RIGHT_STICK_LEFT")
                self.joystickRightStickLeft = False

            if joystick.get_axis(3) >= 0.5 and not self.joystickRightStickRight:
                self.applicationContext.inputObserver.keydown("JOYSTICK_RIGHT_STICK_RIGHT")
                self.joystickRightStickRight = True
            if joystick.get_axis(3) < 0.5 and self.joystickRightStickRight:
                self.applicationContext.inputObserver.keyup("JOYSTICK_RIGHT_STICK_RIGHT")
                self.joystickRightStickRight = False

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
