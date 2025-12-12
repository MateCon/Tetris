from model.piece_generator import PieceGenerator
from model.playfield import Playfield
from model.point import Point
from model.piece_bag import PieceBag


class TetrisGame:
    def __init__(self, aWidth, aHeight, aRandomizer, aRotationListGeneratorClass, aKickAlgorithmClass):
        self.playfield = Playfield(aWidth, aHeight)
        self.randomizer = aRandomizer
        self.kickAlgoritm = aKickAlgorithmClass(self.playfield)
        self.pieceGenerator = PieceGenerator(
            self.playfield,
            self.randomizer,
            aRotationListGeneratorClass(),
            self.kickAlgoritm
        )
        self.currentBag = PieceBag(self.randomizer, self.pieceGenerator)
        self.nextBag = PieceBag(self.randomizer, self.pieceGenerator)
        self.currentPiece = self.currentBag.next()
        self.nextPiece = self.currentBag.next()

    def goToNextBag(self):
        self.currentBag = self.nextBag
        self.nextBag = PieceBag(self.randomizer, self.pieceGenerator)

    def goToNextPiece(self):
        self.currentPiece = self.nextPiece
        if self.currentBag.isEmpty():
            self.goToNextBag()
        self.nextPiece = self.currentBag.next()

    def freezeCurrentPiece(self):
        self.playfield.addBlocks(self.currentPiece)
        self.goToNextPiece()
        self.checkForClearedLines()

    def tick(self):
        self.softDrop()

    def moveRight(self):
        self.currentPiece.move(Point(1, 0))

    def moveLeft(self):
        self.currentPiece.move(Point(-1, 0))

    def rotateRight(self):
        self.currentPiece.rotateRight()

    def rotateLeft(self):
        self.currentPiece.rotateLeft()

    def softDrop(self):
        self.currentPiece.moveIfCantMove(Point(0, -1), self.freezeCurrentPiece)

    def hardDrop(self):
        self.currentPiece.moveIfCanMoveIfCantMove(Point(0, -1), self.hardDrop, self.freezeCurrentPiece)

    def checkForClearedLines(self):
        self.playfield.checkForClearedLines()

    def asStringList(self):
        charMatrix = self.playfield.asCharMatrix()

        def callback(point):
            if self.playfield.pointIsInDisplayableArea(point):
                charMatrix[len(charMatrix) - point.y - 1][point.x] = self.currentPiece.activeCharacter()

        self.currentPiece.do(callback)

        return [''.join(row) for row in charMatrix]

    def getNextPiece(self):
        return self.nextPiece

    def getCurrentBag(self):
        return self.currentBag

    def getNextBag(self):
        return self.nextBag
