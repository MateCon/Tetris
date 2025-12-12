class PieceBag:
    def __init__(self, aRandomizer, aPieceGenerator):
        self.pieceGenerator = aPieceGenerator
        self.pieces = [self.pieceGenerator.nextPiece(index) for index in aRandomizer.nextOrdering(7)]
        self.currentIndex = -1

    def next(self):
        self.currentIndex += 1
        return self.pieces[self.currentIndex]

    def isEmpty(self):
        return self.currentIndex == len(self.pieces) - 1

    def isActiveCharacterAt(self, anIndex, aCharacter):
        return self.pieces[anIndex].activeCharacter() == aCharacter
