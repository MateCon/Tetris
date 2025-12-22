from tetris_model.point import Point


class Piece:
    def __init__(self, aPosition, aRotationList, aPlayfield, aKickAlgoritm, anActiveCharacter):
        self.position = aPosition
        self.initialPosition = aPosition
        self.rotationList = aRotationList
        self.playfield = aPlayfield
        self.kickAlgoritm = aKickAlgoritm
        self.activeChar = anActiveCharacter

    def do(self, aCallback):
        self.rotationList.currentShape().do(lambda squareOffset: aCallback(self.position + squareOffset))

    def blockPositions(self):
        self.rotationList.currentShape().do(lambda squareOffset: aCallback(self.position + squareOffset))

    def allSatisfy(self, aCallback):
        return self.rotationList.currentShape().allSatisfy(lambda squareOffset: aCallback(self.position + squareOffset))

    def anySatisfy(self, aCallback):
        return self.rotationList.currentShape().anySatisfy(lambda squareOffset: aCallback(self.position + squareOffset))

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

    def moveIfCanMove(self, anOffset, aHandlerWhenCanMove):
        self.moveIfCanMoveIfCantMove(anOffset, aHandlerWhenCanMove, lambda: None)

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

        self.kickAlgoritm.rotate(self, self.rotationList.shapeToTheRight(), rotateRightWithOffset, self.rotationList.position(), self.rotationList.positionToTheRight())

    def rotateLeft(self):
        def rotateLeftWithOffset(anOffset):
            self.position = self.position + anOffset
            self.rotationList.rotateLeft()

        self.kickAlgoritm.rotate(self, self.rotationList.shapeToTheLeft(), rotateLeftWithOffset, self.rotationList.position(), self.rotationList.positionToTheLeft())

    def asStringList(self):
        if self.activeCharacter() == "I":
            return ["....", "IIII", "...."]

        charMatrix = [['.' for _ in range(4)] for _ in range(3)]

        def callback(point):
            charMatrix[len(charMatrix) - point.y - 1][point.x] = self.activeCharacter()

        self.rotationList.currentShape().do(callback)

        return [''.join(row) for row in charMatrix]

    def ghost(self):
        ghost = Piece(self.position, self.rotationList, self.playfield, self.kickAlgoritm, self.activeChar)

        def drop():
            ghost.moveIfCanMove(Point(0, -1), drop)

        drop()

        return ghost

    def resetPosition(self):
        self.position = self.initialPosition

    def resetRotation(self):
        self.rotationList.reset()

    def cornersForTSpin(self):
        corners = []
        for offset in self.rotationList.currentShape().offsetsForTSpinCorners():
            corners.append(offset + self.position)
        return corners

    def frontCornersForTSpin(self):
        corners = []
        for offset in self.rotationList.currentShape().offsetsForTSpinFrontCorners():
            corners.append(offset + self.position)
        return corners


class NoPiece:
    def do(self, aCallback):
        pass

    def allSatisfy(self, aCallback):
        return False

    def anySatisfy(self, aCallback):
        return False

    def moveIfCanMoveIfCantMove(self, anOffset, aHandlerWhenCanMove, aHandlerWhenCantMove):
        pass

    def moveIfCanMove(self, anOffset, aHandlerWhenCanMove):
        pass

    def moveIfCantMove(self, anOffset, aHandlerWhenCantMove):
        pass

    def move(self, anOffset):
        pass

    def activeCharacter(self):
        return '.'

    def inactiveCharacter(self):
        return '.'

    def canBlockRotate(self, blockPosition):
        return False

    def canRotate(self, newShape, anOffset):
        return False

    def rotateRight(self):
        pass

    def rotateLeft(self):
        pass

    def asStringList(self):
        return []

    def resetPosition(self):
        pass

    def resetRotation(self):
        pass

    def ghost(self):
        return NoPiece()

    def cornersForTSpin(self):
        return []

    def frontCornersForTSpin(self):
        return []
