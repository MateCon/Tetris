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
        self.clock = pygame.time.Clock()
        self.applicationContext = ApplicationContext(
            pygame.display.set_mode((1280,720)),
            InputObserver()
        )
        self.page = PlayPageComponent(self.applicationContext)
        self.timeSinceLastFrame = 0

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                self.applicationContext.inputObserver.keydown(event.key)
            if event.type == pygame.KEYUP:
                self.applicationContext.inputObserver.keyup(event.key)

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
