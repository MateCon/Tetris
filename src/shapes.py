class Point:
    def __init__(self, anXCoordinate, aYCoordinate):
        self.x = anXCoordinate
        self.y = aYCoordinate

    def plus(self, anotherPoint):
        return Point(self.x + anotherPoint.x, self.y + anotherPoint.y)

    def equals(self, anotherPoint):
        return self.x == anotherPoint.x and self.y == anotherPoint.y
