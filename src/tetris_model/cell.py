from abc import ABC, abstractmethod


class Cell:
    def __init__(self, aPlayfield):
        self.playfield = aPlayfield
        self.state = EmptyCell(self.playfield)

    def occupyWith(self, aPiece):
        self.state = OccupiedCell(aPiece, self.playfield)

    def isOccupied(self):
        return self.state.isOccupied()

    def character(self, aPosition):
        return self.state.character(aPosition)


class CellState(ABC):
    @abstractmethod
    def isOccupied(self) -> bool:
        pass

    @abstractmethod
    def character(self, aPosition) -> str:
        pass


class OccupiedCell(CellState):
    def __init__(self, aPiece, aPlayfield):
        self.piece = aPiece
        self.playfield = aPlayfield

    def isOccupied(self):
        return True

    def character(self, aPosition):
        return self.piece.inactiveCharacter()


class EmptyCell(CellState):
    def __init__(self, aPlayfield):
        self.playfield = aPlayfield

    def isOccupied(self):
        return False

    def character(self, aPosition):
        if aPosition.y >= self.playfield.height:
            return '-'
        return '.'
