from abc import ABC, abstractmethod
from model.point import Point


class WallKickSystem(ABC):
    @abstractmethod
    def rotate(self, aPiece, itsNewShape, rotateWithOffset, position, newPosition):
        pass


class NoKicks(WallKickSystem):
    def __init__(self, aPlayfield):
        self.playfield = aPlayfield

    def rotate(self, aPiece, itsNewShape, rotateWithOffset, position, newPosition):
        origin = Point(0, 0)
        if aPiece.canRotate(itsNewShape, origin):
            rotateWithOffset(origin)


class ARSKicks(WallKickSystem):
    def __init__(self, aPlayfield):
        self.playfield = aPlayfield

    def centerColumnRule(self, aPiece, itsNewShape, anOffset):
        if not aPiece.activeCharacter() in ['L', 'J', 'T']:
            return False

        searchOffsets = [Point(0, 2), Point(1, 2), Point(2, 2),
                         Point(0, 1), Point(1, 1), Point(2, 1),
                         Point(0, 0), Point(1, 0), Point(2, 0)]

        for searchOffset in searchOffsets:
            if self.playfield.hasBlockIn(aPiece.position + searchOffset + anOffset):
                if searchOffset.x == 1:
                    return True
                else:
                    return False

        return False

    def rotate(self, aPiece, itsNewShape, rotateWithOffset, position, newPosition):
        offsets = [Point(0, 0), Point(1, 0), Point(-1, 0)]
        for offset in offsets:
            if aPiece.canRotate(itsNewShape, offset) and not self.centerColumnRule(aPiece, itsNewShape, offset):
                rotateWithOffset(offset)
                return


class SRSKicks(WallKickSystem):
    def __init__(self, aPlayfield):
        self.playfield = aPlayfield
        self.kickOffsetsOfJLSTZ = {
            "0R": [Point(0, 0), Point(-1, 0), Point(-1, 1), Point(0, -2), Point(-1, -2)],
            "R0": [Point(0, 0), Point(1, 0), Point(1, -1), Point(0, 2), Point(1, 2)],
            "R2": [Point(0, 0), Point(1, 0), Point(1, -1), Point(0, 2), Point(1, 2)],
            "2R": [Point(0, 0), Point(-1, 0), Point(-1, 1), Point(0, -2), Point(-1, -2)],
            "2L": [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, -2), Point(1, -2)],
            "L2": [Point(0, 0), Point(-1, 0), Point(-1, -1), Point(0, 2), Point(-1, 2)],
            "L0": [Point(0, 0), Point(-1, 0), Point(-1, -1), Point(0, 2), Point(-1, 2)],
            "0L": [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, -2), Point(1, -2)],
        }
        self.kickOffsetsOfI = {
            "0R": [Point(0, 0), Point(-2, 0), Point(1, 0), Point(-2, -1), Point(1, 2)],
            "R0": [Point(0, 0), Point(2, 0), Point(-1, 0), Point(2, 1), Point(-1, -2)],
            "R2": [Point(0, 0), Point(-1, 0), Point(2, 0), Point(-1, 2), Point(2, -1)],
            "2R": [Point(0, 0), Point(1, 0), Point(-2, 0), Point(1, -2), Point(-2, 1)],
            "2L": [Point(0, 0), Point(2, 0), Point(-1, 0), Point(2, 1), Point(-1, -2)],
            "L2": [Point(0, 0), Point(-2, 0), Point(1, 0), Point(-2, -1), Point(1, 2)],
            "L0": [Point(0, 0), Point(1, 0), Point(-2, 0), Point(1, -2), Point(-2, 1)],
            "0L": [Point(0, 0), Point(-1, 0), Point(2, 0), Point(-1, 2), Point(2, -1)],
        }
        self.kickOffsetsOfO = {
            "0R": [Point(0, 0)],
            "R0": [Point(0, 0)],
            "R2": [Point(0, 0)],
            "2R": [Point(0, 0)],
            "2L": [Point(0, 0)],
            "L2": [Point(0, 0)],
            "L0": [Point(0, 0)],
            "0L": [Point(0, 0)],
        }

    def rotate(self, aPiece, itsNewShape, rotateWithOffset, position, newPosition):
        if aPiece.activeCharacter() == "I":
            offsets = self.kickOffsetsOfI[position + newPosition]
        elif aPiece.activeCharacter() == "O":
            offsets = self.kickOffsetsOfO[position + newPosition]
        else:
            offsets = self.kickOffsetsOfJLSTZ[position + newPosition]
        for offset in offsets:
            if aPiece.canRotate(itsNewShape, offset):
                rotateWithOffset(offset)
                return


