import pygame


class ApplicationContext:
    def __init__(self, aScreen, anInputObserver, aJoystickDictionary, aJoystickLifecycleObserver):
        self.screen = aScreen
        self.inputObserver = anInputObserver
        self.joysticks = aJoystickDictionary
        self.joystickLifecycleObserver = aJoystickLifecycleObserver
        self.isRunning = True

    def drawRect(self, aColor, aRect):
        pygame.draw.rect(self.screen, aColor, aRect)

    def drawText(self, someContents, aColor, aSize, aRect):
        font = pygame.font.Font("assets/fonts/charybdis.regular.ttf", aSize)
        surface = font.render(someContents, True, aColor)
        self.screen.blit(surface, aRect)

    def exit(self):
        self.isRunning = False

