from model.point import Point


class PieceShape:
    def __init__(self, aListOfBlockOffsets, someTSpinOffsets = [Point(0, 0), Point(0, 2), Point(2, 0), Point(2, 2)]):
        self.blockOffsets = aListOfBlockOffsets
        self.tSpinOffsetCorners = someTSpinOffsets

    def do(self, aCallback):
        for blockOffset in self.blockOffsets:
            aCallback(blockOffset)

    def allSatisfy(self, aCallback):
        for blockOffset in self.blockOffsets:
            if not aCallback(blockOffset):
                return False
        return True

    def anySatisfy(self, aCallback):
        for blockOffset in self.blockOffsets:
            if aCallback(blockOffset):
                return True
        return False

    def shifted(self, anOffset):
        newTSpinOffsets = []
        for offset in self.tSpinOffsetCorners:
            newTSpinOffsets.append(offset + anOffset)

        return PieceShape([blockOffset + anOffset for blockOffset in self.blockOffsets], newTSpinOffsets)

    def offsetsForTSpinCorners(self):
        return self.tSpinOffsetCorners

    def offsetsForTSpinFrontCorners(self):
        frontCorners = []
        for corner in self.tSpinOffsetCorners:
            adjacentCount = 0
            for direction in [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]:
                for block in self.blockOffsets:
                    if corner + direction == block:
                        adjacentCount += 1

            if adjacentCount == 2:
                frontCorners.append(corner)

        return frontCorners
