from model.point import Point


class RotationList:
    def __init__(self, aListOfPieceShapes):
        self.pieceShapes = aListOfPieceShapes
        self.currentRotatationIndex = 0

        if self.pieceShapes[0].anySatisfy(lambda offset: offset.y == 2):
            for i in range(len(self.pieceShapes)):
                self.pieceShapes[i] = self.pieceShapes[i].shifted(Point(0, -1))

    def currentShape(self):
        return self.pieceShapes[self.currentRotatationIndex]

    def shiftIndex(self, anOffset):
        self.currentRotatationIndex = (self.currentRotatationIndex + anOffset) % len(self.pieceShapes)

    def rotateRight(self):
        self.shiftIndex(1)

    def shapeToTheRight(self):
        self.rotateRight()
        shape = self.currentShape()
        self.rotateLeft()
        return shape

    def rotateLeft(self):
        self.shiftIndex(-1)

    def shapeToTheLeft(self):
        self.rotateLeft()
        shape = self.currentShape()
        self.rotateRight()
        return shape

    def shiftRotation(self, aRotationIndex, anOffset):
        self.pieceShapes[aRotationIndex] = self.pieceShapes[aRotationIndex].shifted(anOffset)

    def reset(self):
        self.currentRotatationIndex = 0

    def __add__(self, anotherRotationList):
        return RotationList(self.pieceShapes + anotherRotationList.pieceShapes)
