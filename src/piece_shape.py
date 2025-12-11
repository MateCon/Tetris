class PieceShape:
    def __init__(self, aListOfBlockOffsets):
        self.blockOffsets = aListOfBlockOffsets

    def do(self, aCallback):
        for blockOffset in self.blockOffsets:
            aCallback(blockOffset)

    def allSatisfy(self, aCallback):
        for blockOffset in self.blockOffsets:
            if not aCallback(blockOffset):
                return False
        return True

    def shifted(self, anOffset):
        return PieceShape([blockOffset + anOffset for blockOffset in self.blockOffsets])
