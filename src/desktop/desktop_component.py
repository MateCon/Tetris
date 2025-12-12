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
        self.applicationContext.drawRect(self.borderColor, anArea.asRect())
        newArea = anArea.withPadding(self.borderWidth, self.borderWidth)
        self.applicationContext.drawRect(self.backgroundColor, newArea.asRect())
        return newArea

    def drawBorderAround(self, anArea):
        newArea = anArea.withPadding(-self.borderWidth, -self.borderWidth)
        leftArea = Area(newArea.x, newArea.y, self.borderWidth, newArea.height)
        rightArea = Area(newArea.x + newArea.width - self.borderWidth, newArea.y, self.borderWidth, newArea.height)
        topArea = Area(newArea.x, newArea.y, newArea.width, self.borderWidth)
        bottomArea = Area(newArea.x, newArea.y + newArea.height - self.borderWidth, newArea.width, self.borderWidth)
        self.applicationContext.drawRect(self.borderColor, leftArea.asRect())
        self.applicationContext.drawRect(self.borderColor, rightArea.asRect())
        self.applicationContext.drawRect(self.borderColor, topArea.asRect())
        self.applicationContext.drawRect(self.borderColor, bottomArea.asRect())
