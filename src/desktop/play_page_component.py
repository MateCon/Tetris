from desktop.desktop_component import DesktopComponent
from desktop.tetris_game_component import TetrisGameComponent
import pygame


class PlayPageComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self.gameComponent = TetrisGameComponent(anApplicationContext)

    def draw(self, anArea):
        self.applicationContext.drawRect(pygame.Color(0,0,0), anArea.asRect())
        self.gameComponent.draw(anArea)

    def update(self, millisecondsSinceLastUpdate):
        self.gameComponent.update(millisecondsSinceLastUpdate)
