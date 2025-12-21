from model.piece_generator import PieceGenerator
from model.playfield import Playfield
from model.point import Point
from model.piece_bag import PieceBag
from model.tetris_event_notifier import TetrisEventNotifier
from model.piece import NoPiece


class TetrisGame:
    def __init__(
            self,
            aWidth,
            aHeight,
            aRandomizer,
            aRotationListGeneratorClass,
            aKickAlgorithmClass,
            anEventNotifier=TetrisEventNotifier()
    ):
        self.playfield = Playfield(aWidth, aHeight, anEventNotifier)
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
        self.eventNotifier = anEventNotifier
        self.pieceHeld = NoPiece()
        self.canHoldPiece = True
        self.lastActionWasATSpin = False
        self.lastActionWasAMiniTSpin = False

    def goToNextBag(self):
        self.currentBag = self.nextBag
        self.nextBag = PieceBag(self.randomizer, self.pieceGenerator)

    def goToNextPiece(self):
        self.currentPiece = self.nextPiece
        if self.currentBag.isEmpty():
            self.goToNextBag()
        self.nextPiece = self.currentBag.next()
        self.canHoldPiece = True
        self.lastActionWasATSpin = False
        self.lastActionWasAMiniTSpin = False

    def freezeCurrentPiece(self):
        self.playfield.addBlocks(self.currentPiece)
        if self.currentPiece.anySatisfy(lambda point: self.playfield.pointIsInVanishingZone(point)):
            self.eventNotifier.notifyLost()
            self.currentPiece = NoPiece()
        else:
            if self.lastActionWasATSpin:
                self.eventNotifier.notifyTSpin()
            if self.lastActionWasAMiniTSpin:
                self.eventNotifier.notifyMiniTSpin()
            self.checkForClearedLines()
            self.goToNextPiece()
        self.eventNotifier.notifyPlacedPiece()

    def tick(self):
        self.currentPiece.moveIfCantMove(Point(0, -1), self.freezeCurrentPiece)

    def moveRight(self):
        self.currentPiece.move(Point(1, 0))

    def moveLeft(self):
        self.currentPiece.move(Point(-1, 0))

    def rotateRight(self):
        self.currentPiece.rotateRight()
        self.detectTSpin()

    def rotateLeft(self):
        self.currentPiece.rotateLeft()
        self.detectTSpin()

    def detectTSpin(self):
        if self.activeCharacter() != "T":
            return

        cornersOccupied = 0
        for corner in self.currentPiece.cornersForTSpin():
            if self.playfield.hasBlockIn(corner) or not self.playfield.pointIsInPlayfield(corner):
                cornersOccupied += 1

        frontCornersOccupied = 0
        for corner in self.currentPiece.frontCornersForTSpin():
            if self.playfield.hasBlockIn(corner) or not self.playfield.pointIsInPlayfield(corner):
                frontCornersOccupied += 1

        if cornersOccupied == 3:
            if frontCornersOccupied == 2:
                self.lastActionWasATSpin = True
            else:
                self.lastActionWasAMiniTSpin = True

    def softDrop(self):
        self.currentPiece.moveIfCanMoveIfCantMove(Point(0, -1), self.eventNotifier.notifySoftDrop, self.freezeCurrentPiece)

    def hardDrop(self):
        self.blocksInLastHardDrop = -1
        self.hardDropRecursively()
        self.eventNotifier.notifyHardDrop(self.blocksInLastHardDrop)

    def hardDropRecursively(self):
        self.blocksInLastHardDrop += 1
        self.currentPiece.moveIfCanMoveIfCantMove(Point(0, -1), self.hardDropRecursively, self.freezeCurrentPiece)

    def hold(self):
        if not self.canHoldPiece or isinstance(self.currentPiece, NoPiece):
            return
        self.currentPiece.resetPosition()
        self.currentPiece.resetRotation()
        if isinstance(self.pieceHeld, NoPiece):
            self.pieceHeld = self.currentPiece
            self.goToNextPiece()
        else:
            previousPieceHeld = self.pieceHeld
            self.pieceHeld = self.currentPiece
            self.currentPiece = previousPieceHeld
            self.canHoldPiece = False

    def getHeldPiece(self):
        return self.pieceHeld

    def checkForClearedLines(self):
        self.playfield.checkForClearedLines()

    def asCharMatrix(self):
        charMatrix = self.playfield.asCharMatrix()

        def callback(point):
            if self.playfield.pointIsInDisplayableArea(point):
                charMatrix[len(charMatrix) - point.y - 1][point.x] = self.currentPiece.activeCharacter()

        self.currentPiece.do(callback)

        return charMatrix

    def asStringList(self):
        return [''.join(row) for row in self.asCharMatrix()]

    def asStringListWithGhostPiece(self):
        charMatrix = self.asCharMatrix()

        def callback(point):
            if self.playfield.pointIsInDisplayableArea(point):
                previousPiece = charMatrix[len(charMatrix) - point.y - 1][point.x]
                if not previousPiece.isupper():
                    charMatrix[len(charMatrix) - point.y - 1][point.x] = '#'

        self.currentPiece.ghost().do(callback)

        return [''.join(row) for row in charMatrix]

    def getNextPiece(self):
        return self.nextPiece

    def getCurrentBag(self):
        return self.currentBag

    def getNextBag(self):
        return self.nextBag

    def getNextSix(self):
        allRemaining = [self.nextPiece] + self.currentBag.allRemaining() + self.nextBag.allRemaining()
        return allRemaining[0:6]

    def activeCharacter(self):
        return self.currentPiece.activeCharacter()
