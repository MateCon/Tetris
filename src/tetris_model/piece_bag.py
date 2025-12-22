class PieceBag:
    def __init__(self, aRandomizer, aPieceGenerator):
        self.pieceGenerator = aPieceGenerator
        self.pieces = [self.pieceGenerator.nextPiece(index) for index in aRandomizer.nextOrdering(7)]
        self.currentIndex = 0

    def next(self):
        piece = self.pieces[self.currentIndex]
        self.currentIndex += 1
        return piece

    def allRemaining(self):
        return self.pieces[self.currentIndex:]

    def isEmpty(self):
        return self.currentIndex == len(self.pieces)

    def isActiveCharacterAt(self, anIndex, aCharacter):
        return self.pieces[anIndex].activeCharacter() == aCharacter
