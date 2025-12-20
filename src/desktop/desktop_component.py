from abc import ABC, abstractmethod
from desktop.area import Area


class DesktopComponent(ABC):
    def __init__(self, anApplicationContext):
        self.applicationContext = anApplicationContext
        self.backgroundColor = (0, 0, 0)
        self.borderColor = (255, 255, 255)
        self.borderWidth = 0

    @abstractmethod
    def draw(self, anArea):
        pass

    @abstractmethod
    def update(self, millisecondsSinceLastUpdate):
        pass

    def drawBorder(self, anArea) -> Area:
        self.applicationContext.drawArea(self.borderColor, anArea)
        newArea = anArea.withPadding(self.borderWidth, self.borderWidth)
        self.applicationContext.drawArea(self.backgroundColor, newArea)
        return newArea

    def drawBorderAround(self, anArea):
        newArea = anArea.withPadding(-self.borderWidth, -self.borderWidth)
        leftArea = Area(newArea.x, newArea.y, self.borderWidth, newArea.height)
        rightArea = Area(newArea.x + newArea.width - self.borderWidth, newArea.y, self.borderWidth, newArea.height)
        topArea = Area(newArea.x, newArea.y, newArea.width, self.borderWidth)
        bottomArea = Area(newArea.x, newArea.y + newArea.height - self.borderWidth, newArea.width, self.borderWidth)
        self.applicationContext.drawArea(self.borderColor, leftArea)
        self.applicationContext.drawArea(self.borderColor, rightArea)
        self.applicationContext.drawArea(self.borderColor, topArea)
        self.applicationContext.drawArea(self.borderColor, bottomArea)
