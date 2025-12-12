class Piece:
    def __init__(self, aPosition, aRotationList, aPlayfield, aKickAlgoritm, anActiveCharacter):
        self.position = aPosition
        self.rotationList = aRotationList
        self.playfield = aPlayfield
        self.kickAlgoritm = aKickAlgoritm
        self.activeChar = anActiveCharacter

    def do(self, aCallback):
        self.rotationList.currentShape().do(lambda squareOffset: aCallback(self.position + squareOffset))

    def allSatisfy(self, aCallback):
        return self.rotationList.currentShape().allSatisfy(lambda squareOffset: aCallback(self.position + squareOffset))

    def canBlockGoTo(self, aPosition):
        return self.playfield.pointIsInPlayfield(aPosition) and not self.playfield.hasBlockIn(aPosition)

    def canBlockMove(self, blockPosition, anOffset):
        return self.canBlockGoTo(blockPosition + anOffset)

    def canMove(self, anOffset):
        return self.allSatisfy(lambda blockPosition: self.canBlockMove(blockPosition, anOffset))

    def moveIfCanMoveIfCantMove(self, anOffset, aHandlerWhenCanMove, aHandlerWhenCantMove):
        if self.canMove(anOffset):
            self.position = self.position + anOffset
            aHandlerWhenCanMove()
        else:
            aHandlerWhenCantMove()

    def moveIfCantMove(self, anOffset, aHandlerWhenCantMove):
        self.moveIfCanMoveIfCantMove(anOffset, lambda: None, aHandlerWhenCantMove)

    def move(self, anOffset):
        self.moveIfCantMove(anOffset, lambda: None)

    def activeCharacter(self):
        return self.activeChar

    def inactiveCharacter(self):
        return self.activeChar.lower()

    def canBlockRotate(self, blockPosition):
        return self.canBlockGoTo(self.position + blockPosition)

    def canRotate(self, newShape, anOffset):
        return newShape.allSatisfy(lambda blockPosition: self.canBlockRotate(blockPosition + anOffset))

    def rotateRight(self):
        def rotateRightWithOffset(anOffset):
            self.position = self.position + anOffset
            self.rotationList.rotateRight()

        self.kickAlgoritm.rotate(self, self.rotationList.shapeToTheRight(), rotateRightWithOffset)

    def rotateLeft(self):
        def rotateLeftWithOffset(anOffset):
            self.position = self.position + anOffset
            self.rotationList.rotateLeft()

        self.kickAlgoritm.rotate(self, self.rotationList.shapeToTheLeft(), rotateLeftWithOffset)
