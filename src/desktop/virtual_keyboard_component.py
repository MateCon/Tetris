from desktop.desktop_component import DesktopComponent
from tetris_model.point import Point
from desktop.area import Area


class VirtualKeyboardComponent(DesktopComponent):
    def __init__(self, anApplicationContext):
        super().__init__(anApplicationContext)
        self._isOpen = False
        self.borderWidth = 2
        self.keys = [
            ["1","2","3","4","5","6","7","8","9","0"],
            ["q","w","e","r","t","y","u","i","o","p"],
            ["a","s","d","f","g","h","j","k","l", "<"],
            ["z","x","c","v","b","n","m", "accept"]
        ]
        self.position = Point(0, 2)

    def isOpen(self):
        return self._isOpen

    def openWith(self, anInput):
        self.position = Point(0, 2)
        self._isOpen = True
        self._input = anInput

    def close(self):
        self._isOpen = False
        self._input.stopEditing()

    def moveUp(self):
        self.position.y = (self.position.y - 1) % len(self.keys)

    def moveDown(self):
        self.position.y = (self.position.y + 1) % len(self.keys)

    def realPosition(self):
        return Point(min(self.position.x, len(self.keys[self.position.y]) - 1), self.position.y)

    def moveLeft(self):
        self.position.x = (self.realPosition().x - 1) % len(self.keys[self.position.y])

    def moveRight(self):
        self.position.x = (self.realPosition().x + 1) % len(self.keys[self.position.y])

    def accept(self):
        key = self.keys[self.realPosition().y][self.realPosition().x]
        if key == "<":
            self._input.delete()
        elif key == "accept":
            self._input.closeKeyboard()
        else:
            self._input.write(key)

    def draw(self, anArea):
        if not self._isOpen:
            return
        self.drawBorderAround(anArea)
        keySize = Point(anArea.width // 10, anArea.height // 4)
        keyArea = Area(0, 0, keySize.x, keySize.y)
        for y, row in enumerate(self.keys):
            for x, key in enumerate(row):
                currentArea = anArea.shifted(x * keySize.x, y * keySize.y)
                currentArea.width = keyArea.width
                currentArea.height = keyArea.height
                if Point(x, y) == self.realPosition():
                    if key == "accept":
                        currentArea.width *= 3
                    self.applicationContext.drawArea((255, 255, 255), currentArea)
                    textColor = (0, 0, 0)
                else:
                    light = 255 - ((abs(x - self.realPosition().x) + abs(y - self.realPosition().y)) * 20)
                    textColor = (light, light, light)
                self.applicationContext.drawText(key, textColor, 22, currentArea.shifted(8, 0))

    def update(self, millisecondsSinceLastUpdate):
        pass
