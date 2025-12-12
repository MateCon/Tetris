from model.piece import Piece
from model.point import Point


class PieceGenerator:
    def __init__(self, aPlayfield, aRandomizer, aRotationListGenerator, aKickAlgorithm):
        self.playfield = aPlayfield
        self.randomizer = aRandomizer
        self.rotationListGenerator = aRotationListGenerator
        self.kickAlgorithm = aKickAlgorithm

    def createIPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(4, 1)),
            self.rotationListGenerator.createIRotationList(),
            self.playfield,
            self.kickAlgorithm,
            "I")

    def createJPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            self.rotationListGenerator.createJRotationList(),
            self.playfield,
            self.kickAlgorithm,
            "J")

    def createLPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            self.rotationListGenerator.createLRotationList(),
            self.playfield,
            self.kickAlgorithm,
            "L")

    def createOPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(2, 2)),
            self.rotationListGenerator.createORotationList(),
            self.playfield,
            self.kickAlgorithm,
            "O")

    def createSPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            self.rotationListGenerator.createSRotationList(),
            self.playfield,
            self.kickAlgorithm,
            "S")

    def createZPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            self.rotationListGenerator.createZRotationList(),
            self.playfield,
            self.kickAlgorithm,
            "Z")

    def createTPiece(self):
        return Piece(
            self.playfield.pieceStartingPositionWithDimensions(Point(3, 2)),
            self.rotationListGenerator.createTRotationList(),
            self.playfield,
            self.kickAlgorithm,
            "T")

    def nextPiece(self):
        nextInteger = self.randomizer.nextInteger(1, 7) - 1
        pieces = [
            self.createIPiece,
            self.createJPiece,
            self.createLPiece,
            self.createOPiece,
            self.createSPiece,
            self.createZPiece,
            self.createTPiece
        ]
        return pieces[nextInteger]()
