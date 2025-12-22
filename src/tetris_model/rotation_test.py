from tetris_model.tetris_game import TetrisGame
from tetris_model.rotation_list_generator import NintendoRotationListGenerator, SegaRotationListGenerator, SuperRotationListGenerator
from tetris_model.rand import RandStub
from tetris_model.kicks import NoKicks


class TestNintendoRotationSystem:
    def test01_IPieceRotatesRightOnce(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "-----I----",
            "-----I----",
            ".....I....",
            ".....I....",
            "..........",
            "..........",
        ]

    def test02_PieceCanRotateAboveVanishZone(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateRight()

        assert game.asStringList() == [
            "-----I----",
            "-----I----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test03_IPieceRotatesRightMoreThanOnce(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test04_IPieceRotatesLeftOnce(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateLeft()

        assert game.asStringList() == [
            "-----I----",
            "-----I----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test05_IPieceRotatesLeftMoreThanOnce(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateLeft()
        game.rotateLeft()
        game.rotateLeft()
        game.rotateLeft()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test06_JPieceRotatesRightOnce(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "----J-----",
            "----J-----",
            "...JJ.....",
            "..........",
            "..........",
            "..........",
        ]

    def test07_JPieceRotatesRightTwice(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "---J------",
            "---JJJ----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test08_JPieceRotatesRightThrice(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()
        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "----JJ----",
            "----J-----",
            "....J.....",
            "..........",
            "..........",
            "..........",
        ]

    def test09_TPieceRotatesRightOnce(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "---TT-----",
            "....T.....",
            "..........",
            "..........",
            "..........",
        ]

    def test10_TPieceRotatesRightTwice(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "---TTT----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test11_TPieceRotatesRightThrice(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()
        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "----TT----",
            "....T.....",
            "..........",
            "..........",
            "..........",
        ]

    def test12_SPieceRotatesRight(self):
        random = RandStub([5])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "----S-----",
            "----SS----",
            ".....S....",
            "..........",
            "..........",
            "..........",
        ]

    def test13_ZPieceRotatesRight(self):
        random = RandStub([6])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "-----Z----",
            "----ZZ----",
            "....Z.....",
            "..........",
            "..........",
            "..........",
        ]

    def test14_ZPieceRotatesRightOnce(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "---TT-----",
            "....T.....",
            "..........",
            "..........",
            "..........",
        ]

    def test15_ZPieceRotatesRightTwice(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "---TTT----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test16_ZPieceRotatesRightThrice(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()
        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "----TT----",
            "....T.....",
            "..........",
            "..........",
            "..........",
        ]


class TestNoWallKicks:
    def test01_PieceCantRotateRightIfABlockWillBeOutOfThePlayfild(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.rotateRight()

        assert game.asStringList() == [
            "---------I",
            "---------I",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test02_PieceCantRotateLeftIfABlockWillBeOutOfThePlayfild(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.rotateLeft()

        assert game.asStringList() == [
            "---------I",
            "---------I",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test03_PieceCantRotateIfABlockWillBeInAnOccupiedCell(self):
        random = RandStub([1, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateRight()
        game.moveRight()
        game.hardDrop()

        game.rotateRight()
        game.softDrop()
        game.softDrop()
        game.rotateRight()

        assert game.asStringList() == [
            "-----I----",
            "-----I----",
            ".....Ii...",
            ".....Ii...",
            "......i...",
            "......i...",
        ]


class TestSuperRotationSystem:
    def test01_IPieceStartsHigherThanNintendo(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.tick()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test02_IPieceRotatesLikeNintendo(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.tick()
        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "-----I----",
            "-----I----",
            ".....I....",
            ".....I....",
            "..........",
            "..........",
        ]

    def test03_JPieceRotatesLikeNintendo(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "----J-----",
            "----J-----",
            "...JJ.....",
            "..........",
            "..........",
            "..........",
        ]

    def test04_JPieceRotatesTwiceLowerThanNintendo(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "---J------",
            "---JJJ----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test05_LPieceRotatesLikeNintendo(self):
        random = RandStub([3])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "---LL-----",
            "----L-----",
            "....L.....",
            "..........",
            "..........",
            "..........",
        ]

    def test06_LPieceRotatesTwiceLowerThanNintendo(self):
        random = RandStub([3])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "-----L----",
            "---LLL----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test07_OPieceRotatesLikeNintendo(self):
        random = RandStub([4])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.tick()
        game.tick()
        game.rotateRight()

        assert game.asStringList() == [
            "----------",
            "----------",
            "....OO....",
            "....OO....",
            "..........",
            "..........",
        ]

    def test08_SPieceRotatesStartsLikeNintendo(self):
        random = RandStub([5])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "----SS----",
            "---SS-----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test08_SPieceRotatesOnceToTheLeftOfNintendo(self):
        random = RandStub([5])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.softDrop()
        game.rotateRight()

        assert game.asStringList() == [
            "---S------",
            "---SS-----",
            "....S.....",
            "..........",
            "..........",
            "..........",
        ]

    def test09_ZPieceRotatesLikeNintendo(self):
        random = RandStub([6])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.softDrop()
        game.rotateRight()

        assert game.asStringList() == [
            "-----Z----",
            "----ZZ----",
            "....Z.....",
            "..........",
            "..........",
            "..........",
        ]

    def test10_TPieceRotatesLikeNintendo(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.softDrop()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "---TT-----",
            "....T.....",
            "..........",
            "..........",
            "..........",
        ]

    def test11_TPieceRotatesTwiceLowerThanNintendo(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, NoKicks)

        game.rotateRight()
        game.rotateRight()

        assert game.asStringList() == [
            "----T-----",
            "---TTT----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]


class TestSegaRotationSystem:
    def test01_IPiece(self):
        random = RandStub([1])
        game = TetrisGame(4, 2, random, SuperRotationListGenerator, NoKicks)

        game.tick()

        assert game.asStringList() == [
            "----",
            "IIII",
            "....",
            "....",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "--I-",
            "--I-",
            "..I.",
            "..I.",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "----",
            "----",
            "IIII",
            "....",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-I--",
            "-I--",
            ".I..",
            ".I..",
        ]

    def test02_JPiece(self):
        random = RandStub([2])
        game = TetrisGame(3, 1, random, SuperRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "J--",
            "JJJ",
            "...",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-JJ",
            "-J-",
            ".J.",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "---",
            "JJJ",
            "..J",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-J-",
            "-J-",
            "JJ.",
        ]

    def test03_LPiece(self):
        random = RandStub([3])
        game = TetrisGame(3, 1, random, SuperRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "--L",
            "LLL",
            "...",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-L-",
            "-L-",
            ".LL",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "---",
            "LLL",
            "L..",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "LL-",
            "-L-",
            ".L.",
        ]

    def test04_OPiece(self):
        random = RandStub([4])
        game = TetrisGame(4, 2, random, SuperRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "-OO-",
            "-OO-",
            "....",
            "....",
        ]

    def test05_LPiece(self):
        random = RandStub([5])
        game = TetrisGame(3, 1, random, SuperRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "-SS",
            "SS-",
            "...",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-S-",
            "-SS",
            "..S",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "---",
            "-SS",
            "SS.",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "S--",
            "SS-",
            ".S.",
        ]

    def test06_ZPiece(self):
        random = RandStub([6])
        game = TetrisGame(3, 1, random, SuperRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "ZZ-",
            "-ZZ",
            "...",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "--Z",
            "-ZZ",
            ".Z.",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "---",
            "ZZ-",
            ".ZZ",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-Z-",
            "ZZ-",
            "Z..",
        ]

    def test07_TPiece(self):
        random = RandStub([7])
        game = TetrisGame(3, 1, random, SuperRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "-T-",
            "TTT",
            "...",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-T-",
            "-TT",
            ".T.",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "---",
            "TTT",
            ".T.",
        ]

        game.rotateRight()

        assert game.asStringList() == [
            "-T-",
            "TT-",
            ".T.",
        ]
