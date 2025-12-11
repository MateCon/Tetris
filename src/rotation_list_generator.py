from rotation_list import RotationList
from piece_shape import PieceShape
from point import Point


class NintendoRotationListGenerator:
    def createIRotationList(self):
        return RotationList([
            PieceShape([Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1)]),
            PieceShape([Point(2, 0), Point(2, 1), Point(2, 2), Point(2, 3)]),
        ])

    def createJRotationList(self):
        return RotationList([
            PieceShape([Point(0, 1), Point(1, 1), Point(2, 1), Point(2, 0)]),
            PieceShape([Point(0, 0), Point(1, 0), Point(1, 1), Point(1, 2)]),
            PieceShape([Point(0, 1), Point(1, 1), Point(2, 1), Point(0, 2)]),
            PieceShape([Point(1, 0), Point(1, 1), Point(1, 2), Point(2, 2)]),
        ])

    def createLRotationList(self):
        return RotationList([
            PieceShape([Point(0, 0), Point(0, 1), Point(1, 1), Point(2, 1)]),
            PieceShape([Point(0, 2), Point(1, 2), Point(1, 1), Point(1, 0)]),
            PieceShape([Point(0, 1), Point(1, 1), Point(2, 1), Point(2, 2)]),
            PieceShape([Point(1, 0), Point(2, 0), Point(1, 1), Point(1, 2)]),
        ])

    def createORotationList(self):
        return RotationList([
            PieceShape([Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)]),
        ])

    def createSRotationList(self):
        return RotationList([
            PieceShape([Point(0, 0), Point(1, 0), Point(1, 1), Point(2, 1)]),
            PieceShape([Point(1, 2), Point(1, 1), Point(2, 1), Point(2, 0)]),
        ])

    def createZRotationList(self):
        return RotationList([
            PieceShape([Point(0, 1), Point(1, 1), Point(1, 0), Point(2, 0)]),
            PieceShape([Point(1, 0), Point(1, 1), Point(2, 1), Point(2, 2)]),
        ])

    def createTRotationList(self):
        return RotationList([
            PieceShape([Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 0)]),
            PieceShape([Point(0, 1), Point(1, 0), Point(1, 1), Point(1, 2)]),
            PieceShape([Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2)]),
            PieceShape([Point(1, 0), Point(1, 1), Point(2, 1), Point(1, 2)]),
        ])


class SegaRotationListGenerator:
    def __init__(self):
        self.nintendoRotationListGenerator = NintendoRotationListGenerator()

    def createIRotationList(self):
        rotationList = self.nintendoRotationListGenerator.createIRotationList()
        rotationList.shiftRotation(0, Point(0, 1))
        return rotationList

    def createJRotationList(self):
        rotationList = self.nintendoRotationListGenerator.createJRotationList()
        rotationList.shiftRotation(2, Point(0, -1))
        return rotationList

    def createLRotationList(self):
        rotationList = self.nintendoRotationListGenerator.createLRotationList()
        rotationList.shiftRotation(2, Point(0, -1))
        return rotationList

    def createORotationList(self):
        return self.nintendoRotationListGenerator.createORotationList()

    def createSRotationList(self):
        rotationList = self.nintendoRotationListGenerator.createSRotationList()
        rotationList.shiftRotation(1, Point(-1, 0))
        return rotationList

    def createZRotationList(self):
        return self.nintendoRotationListGenerator.createZRotationList()

    def createTRotationList(self):
        rotationList = self.nintendoRotationListGenerator.createTRotationList()
        rotationList.shiftRotation(2, Point(0, -1))
        return rotationList
