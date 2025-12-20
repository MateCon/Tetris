import pygame


class ApplicationContext:
    def __init__(self, aScreen, anInputObserver, aJoystickDictionary, aJoystickLifecycleObserver):
        self.screen = aScreen
        self.inputObserver = anInputObserver
        self.joysticks = aJoystickDictionary
        self.joystickLifecycleObserver = aJoystickLifecycleObserver
        self.isRunning = True

    def drawArea(self, aColor, anArea):
        pygame.draw.rect(self.screen, aColor, anArea.asRect())

    def drawText(self, someContents, aColor, aSize, anArea):
        font = pygame.font.Font("assets/fonts/charybdis.regular.ttf", aSize)
        surface = font.render(someContents, True, aColor)
        self.screen.blit(surface, anArea.asRect())

    def exit(self):
        self.isRunning = False

