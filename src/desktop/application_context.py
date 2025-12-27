import pygame


class ApplicationContext:
    def __init__(self, aScreen, aFrameRate, anApiUrl, anInputObserver, aJoystickDictionary, aJoystickLifecycleObserver, aResourcePathMethod, someSavedSessions):
        self.screen = aScreen
        self.frameRate = aFrameRate
        self.apiUrl = anApiUrl
        self.inputObserver = anInputObserver
        self.joysticks = aJoystickDictionary
        self.joystickLifecycleObserver = aJoystickLifecycleObserver
        self.resourcePathMethod = aResourcePathMethod
        self.savedSessions = someSavedSessions
        self.isRunning = True

    def drawArea(self, aColor, anArea):
        pygame.draw.rect(self.screen, aColor, anArea.asRect())

    def drawText(self, someContents, aColor, aSize, anArea):
        font = pygame.font.Font(self.resourcePathMethod("assets/fonts/charybdis.regular.ttf"), aSize)
        surface = font.render(someContents, True, aColor)
        self.screen.blit(surface, anArea.asRect())

    def exit(self):
        self.isRunning = False

