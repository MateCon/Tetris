import pygame


class ApplicationContext:
    def __init__(self, aScreen, anInputObserver, aBigFont):
        self.screen = aScreen
        self.inputObserver = anInputObserver
        self.bigFont = aBigFont

    def drawRect(self, aColor, aRect):
        pygame.draw.rect(self.screen, aColor, aRect)

    def drawBigText(self, someContents, aColor, aRect):
        surface = self.bigFont.render(someContents, True, aColor)
        self.screen.blit(surface, aRect)

