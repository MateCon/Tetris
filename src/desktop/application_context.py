import pygame


class ApplicationContext:
    def __init__(self, aScreen, anInputObserver):
        self.screen = aScreen
        self.inputObserver = anInputObserver

    def drawRect(self, aColor, aRect):
        pygame.draw.rect(self.screen, aColor, aRect)
