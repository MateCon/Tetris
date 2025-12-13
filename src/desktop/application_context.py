import pygame


class ApplicationContext:
    def __init__(self, aScreen, anInputObserver, aBigFont, aJoystickDictionary,aJoystickLifecycleObserver):
        self.screen = aScreen
        self.inputObserver = anInputObserver
        self.bigFont = aBigFont
        self.joysticks = aJoystickDictionary
        self.joystickLifecycleObserver = aJoystickLifecycleObserver

    def drawRect(self, aColor, aRect):
        pygame.draw.rect(self.screen, aColor, aRect)

    def drawBigText(self, someContents, aColor, aRect):
        surface = self.bigFont.render(someContents, True, aColor)
        self.screen.blit(surface, aRect)

