from model.tetris_event_notifier import TetrisEventNotifier
from model.event_notifier import RepeatedObserver
from model.tetris_game import TetrisGame
from model.rotation_list_generator import NintendoRotationListGenerator
from model.rand import RandStub
from model.kicks import NoKicks
import pytest


class TestGameEvents:
    def test01_RowClearedEventIsTriggeredIfARowIsClearedOnce(self):
        random = RandStub([1, 1, 4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.rowCleared = False

        def event():
            self.rowCleared = True

        eventNotifier.attachRowClearEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()
        game.hardDrop()

        assert self.rowCleared

    def test02_RowClearedEventIsNotTriggeredIfNoRowsAreCleared(self):
        random = RandStub([1, 1, 4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachRowClearEvent(event)

    def test03_RowClearedEventIsNotTriggeredIfMoreThanOneRowIsClearedAtTheSameTime(self):
        random = RandStub([4, 4, 4, 4, 4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachRowClearEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

    def test04_RowClearedEventIsTriggeredEveryTimeARowIsCleared(self):
        random = RandStub([1, 1, 4, 1, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.rowsCleared = 0

        def event():
            self.rowsCleared += 1

        eventNotifier.attachRowClearEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()
        game.hardDrop()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        assert self.rowsCleared == 2

    def test05_AllRowClearedEventsAreTriggeredWhenARowIsTriggered(self):
        random = RandStub([1, 1, 4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.rowCleared1 = False
        self.rowCleared2 = False

        def event1():
            self.rowCleared1 = True

        def event2():
            self.rowCleared2 = True

        eventNotifier.attachRowClearEvent(event1)
        eventNotifier.attachRowClearEvent(event2)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()
        game.hardDrop()

        assert self.rowCleared1
        assert self.rowCleared2

    def test06_AnEventCanNotBeAddedTwice(self):
        random = RandStub([1, 1, 4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        def event():
            pass

        eventNotifier.attachRowClearEvent(event)

        with pytest.raises(RepeatedObserver):
            eventNotifier.attachRowClearEvent(event)

    def test07_DoubleRowClearedEventIsTriggered(self):
        random = RandStub([4, 4, 4, 4, 4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.rowCleared = False

        def event():
            self.rowCleared = True

        eventNotifier.attachDoubleRowClearEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        assert self.rowCleared

    def test08_TripleRowClearedEventIsTriggered(self):
        random = RandStub([3, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 6, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.rowCleared = False

        def event():
            self.rowCleared = True

        eventNotifier.attachTripleRowClearEvent(event)

        game.rotateLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        for i in range(9):
            game.rotateRight()
            for _ in range(6):
                game.moveLeft()
            for _ in range(0, i + 1):
                game.moveRight()
            game.hardDrop()

        assert self.rowCleared

    def test09_QuadrupleRowClearedEventIsTriggered(self):
        random = RandStub([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 6, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.rowCleared = False

        def event():
            self.rowCleared = True

        eventNotifier.attachQuadrupleRowClearEvent(event)

        for i in range(10):
            game.rotateRight()
            for _ in range(6):
                game.moveLeft()
            for _ in range(0, i):
                game.moveRight()
            game.hardDrop()

        assert self.rowCleared

    def test10_PlacedPieceEventIsTriggered(self):
        random = RandStub([1, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 6, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.placedPiece = False

        def event():
            self.placedPiece = True

        eventNotifier.attachPlacedPieceEvent(event)

        game.hardDrop()

        assert self.placedPiece

    def test11_ComboBreakEventIsTriggered(self):
        random = RandStub([1, 1, 4, 1, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 6, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.comboBreak  = False

        def event():
            self.comboBreak = True

        eventNotifier.attachComboBreakEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.hardDrop()

        game.hardDrop()

        assert self.comboBreak

    def test12_ComboBreakEventIsNotTriggeredIfALineWasCleared(self):
        random = RandStub([1, 1, 4, 1, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 6, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        def event():
            assert False

        eventNotifier.attachComboBreakEvent(event)

        game.hardDrop()

    def test13_LostEventIsTriggered(self):
        random = RandStub([4, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 1, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.lost = False

        def event():
            self.lost = True

        eventNotifier.attachLostEvent(event)

        game.hardDrop()

        assert self.lost

    def test14_SoftDropEventIsTriggered(self):
        random = RandStub([4, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 1, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.softDrop = False

        def event():
            self.softDrop = True

        eventNotifier.attachSoftDropEvent(event)

        game.softDrop()

        assert self.softDrop

    def test15_SoftDropEventIsNotTriggeredWithTick(self):
        random = RandStub([4, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 1, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachSoftDropEvent(event)

        game.tick()

    def test16_HardDropEventIsTriggeredWithTheAmountOfBlocksItDrops(self):
        random = RandStub([4, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.blocks = 0

        def event(someBlocks):
            self.blocks = someBlocks

        eventNotifier.attachHardDropEvent(event)

        game.hardDrop()

        assert self.blocks == 4


