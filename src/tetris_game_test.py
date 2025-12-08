from tetris_game import TetrisGame
from rand import RandStub


class TestTetrisGame:
    def test01_IPieceSpawnsInTheMiddleWithEvenWidthPlayfield(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random)

        assert game.asStringList() == [
            "---xxxx---",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test02_IPieceSpawnsInTheMiddleWithOddWidthPlayfield(self):
        random = RandStub([1])
        game = TetrisGame(9, 4, random)

        assert game.asStringList() == [
            "--xxxx---",
            "---------",
            ".........",
            ".........",
            ".........",
            ".........",
        ]

    def test03_JPieceSpawnsInTheMiddleWithEvenWidthPlayfield(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random)

        assert game.asStringList() == [
            "---x------",
            "---xxx----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test04_JPieceSpawnsInTheMiddleWithOddWidthPlayfield(self):
        random = RandStub([2])
        game = TetrisGame(7, 4, random)

        assert game.asStringList() == [
            "--x----",
            "--xxx--",
            ".......",
            ".......",
            ".......",
            ".......",
        ]

    def test05_LPieceSpawnsInTheMiddle(self):
        random = RandStub([3])
        game = TetrisGame(10, 4, random)

        assert game.asStringList() == [
            "-----x----",
            "---xxx----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test06_OPieceSpawnsInTheMiddleWithEvenPlayfield(self):
        random = RandStub([4])
        game = TetrisGame(10, 4, random)

        assert game.asStringList() == [
            "----xx----",
            "----xx----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test07_OPieceSpawnsInTheMiddleWithOddPlayfield(self):
        random = RandStub([4])
        game = TetrisGame(11, 4, random)

        assert game.asStringList() == [
            "----xx-----",
            "----xx-----",
            "...........",
            "...........",
            "...........",
            "...........",
        ]

    def test08_SPieceSpawnsInTheMiddle(self):
        random = RandStub([5])
        game = TetrisGame(10, 4, random)

        assert game.asStringList() == [
            "----xx----",
            "---xx-----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test09_ZPieceSpawnsInTheMiddle(self):
        random = RandStub([6])
        game = TetrisGame(10, 4, random)

        assert game.asStringList() == [
            "---xx-----",
            "----xx----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test10_TPieceSpawnsInTheMiddle(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random)

        assert game.asStringList() == [
            "----x-----",
            "---xxx----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test11_PieceMovesDownAfterTick(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random)

        game.tick()

        assert game.asStringList() == [
            "----------",
            "---x------",
            "...xxx....",
            "..........",
            "..........",
            "..........",
        ]

    def test12_NewPieceSpawnsWhenCurrentPieceIsBlockedByGround(self):
        random = RandStub([2, 1])
        game = TetrisGame(10, 4, random)

        game.tick()
        game.tick()
        game.tick()
        game.tick()
        game.tick()

        assert game.asStringList() == [
            "---xxxx---",
            "----------",
            "..........",
            "..........",
            "...x......",
            "...xxx....",
        ]

    def test13_PiecesCanBeStackedOnTopOfEachOther(self):
        random = RandStub([2, 1, 3])
        game = TetrisGame(10, 4, random)

        game.tick()
        game.tick()
        game.tick()
        game.tick()
        game.tick()

        game.tick()
        game.tick()
        game.tick()
        game.tick()

        assert game.asStringList() == [
            "-----x----",
            "---xxx----",
            "..........",
            "...xxxx...",
            "...x......",
            "...xxx....",
        ]
