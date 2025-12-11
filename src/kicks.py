from abc import ABC, abstractmethod
from point import Point


class WallKickSystem(ABC):
    @abstractmethod
    def rotate(self, aPiece, itsNewShape, rotateWithOffset):
        pass


class NoKicks(WallKickSystem):
    def __init__(self, aPlayfield):
        self.playfield = aPlayfield

    def rotate(self, aPiece, itsNewShape, rotateWithOffset):
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

    def rotate(self, aPiece, itsNewShape, rotateWithOffset):
        offsets = [Point(0, 0), Point(1, 0), Point(-1, 0)]
        for offset in offsets:
            if aPiece.canRotate(itsNewShape, offset) and not self.centerColumnRule(aPiece, itsNewShape, offset):
                rotateWithOffset(offset)
                return


