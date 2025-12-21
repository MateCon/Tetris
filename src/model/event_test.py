from model.tetris_event_notifier import TetrisEventNotifier
from model.event_notifier import RepeatedObserver
from model.tetris_game import TetrisGame
from model.rotation_list_generator import NintendoRotationListGenerator, SuperRotationListGenerator
from model.rand import RandStub
from model.kicks import NoKicks, SRSKicks
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

    def test17_TSpinEventIsNotTriggeredUntilThePieceIsFrozen(self):
        random = RandStub([7, 7, 4, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachTSpinEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.hardDrop()

        game.rotateLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateLeft()

    def test18_TSpinEventIsTriggeredWhenThreeCornersAreOccupied(self):
        random = RandStub([7, 7, 4, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        self.tspin = False

        def event():
            self.tspin = True

        eventNotifier.attachTSpinEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.hardDrop()

        game.rotateLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateLeft()
        game.tick()

        assert self.tspin

    def test19_TSpinEventIsNotTriggeredForNonTPieces(self):
        random = RandStub([4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachTSpinEvent(event)

        game.tick()
        game.tick()
        game.tick()
        game.tick()
        game.rotateLeft()
        game.tick()

    def test20_TSpinEventIsNotTriggeredWhenLessThanThreeCornersAreOccupied(self):
        random = RandStub([7, 7, 4, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachTSpinEvent(event)

        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateRight()
        game.tick()

    def test21_TSpinEventIsTriggeredWhenACornerInTheFrontIsNotOccupied(self):
        random = RandStub([7, 7, 4, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachTSpinEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.hardDrop()

        game.rotateLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateRight()
        game.tick()

    def test21_MiniTSpinEventIsTriggered(self):
        random = RandStub([7, 7, 4, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        self.miniTSpin = False

        def event():
            self.miniTSpin = True

        eventNotifier.attachMiniTSpinEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.hardDrop()

        game.rotateLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateRight()
        game.tick()

        assert self.miniTSpin

    def test21_MiniTSpinEventIsNotTriggeredWhenABackCornerIsNotOccupied(self):
        random = RandStub([7, 7, 4, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        def event():
            assert False

        eventNotifier.attachMiniTSpinEvent(event)

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.hardDrop()

        game.rotateLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateLeft()
        game.tick()

    def test21_TSpinEventsAreTriggeredBeforeLineClears(self):
        random = RandStub([1, 4, 7, 7, 4, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, NoKicks, eventNotifier)

        self.spin = False

        def event1():
            self.spin = True

        def event2():
            assert self.spin

        eventNotifier.attachTSpinEvent(event1)
        eventNotifier.attachRowClearEvent(event2)

        game.rotateLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.hardDrop()

        game.rotateLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateLeft()
        game.tick()

    def test22_RowClearedEventsAreTriggeredBeforePlacePieceEvent(self):
        random = RandStub([1, 1, 4])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks, eventNotifier)

        self.rowCleared = False
        self.placedPieceAfterRowClear = False

        def event1():
            self.rowCleared = True

        def event2():
            if self.rowCleared:
                self.placedPieceAfterRowClear = True

        eventNotifier.attachRowClearEvent(event1)
        eventNotifier.attachPlacedPieceEvent(event2)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()
        game.hardDrop()

        assert self.placedPieceAfterRowClear

    def test23_SpinEventsCanUsePiecesOutOfThePlayingFieldAsOccupiedBlocks(self):
        random = RandStub([1, 7, 1])
        eventNotifier = TetrisEventNotifier()
        game = TetrisGame(10, 4, random, SuperRotationListGenerator, SRSKicks, eventNotifier)

        self.spin = False

        def event():
            self.spin = True

        eventNotifier.attachMiniTSpinEvent(event)

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateLeft()

        game.tick()

        assert self.spin
