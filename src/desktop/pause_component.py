from desktop.desktop_component import DesktopComponent
import pygame


class PauseComponent(DesktopComponent):
    def __init__(self, anApplicationContext, aGameComponent, aCellSize, aRestartMethod, aDeleteMethod):
        self.applicationContext = anApplicationContext
        self.gameComponent = aGameComponent
        self.cellSize = aCellSize
        self.restartMethod = aRestartMethod
        self.deleteMethod = aDeleteMethod
        self.currentOptionIndex = 0
        self.options = [("Resume", self.resume), ("Restart", self.restart), ("Remove Device", self.removeDevice), ("Exit", self.exit)]
        self.hasLost = False
        self.gameComponent.tetrisEventNotifier.attachLostEvent(self.onLost)

    def accept(self):
        self.options[self.currentOptionIndex][1]()

    def resume(self):
        self.gameComponent.togglePause()

    def restart(self):
        self.restartMethod()

    def removeDevice(self):
        self.deleteMethod()

    def exit(self):
        self.applicationContext.exit()

    def moveDown(self):
        self.currentOptionIndex += 1
        self.currentOptionIndex = self.currentOptionIndex % len(self.options)

    def moveUp(self):
        self.currentOptionIndex -= 1
        self.currentOptionIndex = self.currentOptionIndex % len(self.options)

    def focusRestart(self):
        for index, (text, action) in enumerate(self.options):
            if text == "Restart":
                self.currentOptionIndex = index

    def onLost(self):
        self.hasLost = True

    def lost(self):
        return self.hasLost

    def draw(self, anArea):
        currentArea = anArea.copy().shifted(0, self.cellSize * 7)
        totalArea = currentArea
        currentArea.height = 40
        textXOffset = anArea.width / 2 - 65
        title = "Paused"
        if self.hasLost:
            title = "LOST"
        self.applicationContext.drawArea((0, 0, 0), currentArea)
        self.applicationContext.drawText(title, (255, 255, 255), 38, currentArea.shifted(textXOffset, 0))
        currentArea = currentArea.shifted(0, 40)
        currentArea.height = 30
        for index, (text, action) in enumerate(self.options):
            if index == self.currentOptionIndex:
                textColor = (0, 0, 0)
                rectColor = (255, 255, 255)
            else:
                textColor = (255, 255, 255)
                rectColor = (0, 0, 0)
            self.applicationContext.drawArea(rectColor, currentArea)
            self.applicationContext.drawText(text, textColor, 24, currentArea.shifted(textXOffset, 0))
            currentArea = currentArea.shifted(0, 30)
        totalArea.height = currentArea.y - totalArea.y
        self.backgroundColor = (0, 0, 0)
        self.borderWidth = 2
        self.borderColor = (255, 255, 255)
        self.drawBorderAround(totalArea)

    def update(self, millisecondsSinceLastUpdate):
        pass
