class RotationList:
    def __init__(self, aListOfPieceShapes):
        self.pieceShapes = aListOfPieceShapes
        self.currentRotatationIndex = 0

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
