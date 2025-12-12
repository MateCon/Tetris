from model.tetris_game import TetrisGame
from model.rotation_list_generator import NintendoRotationListGenerator, SegaRotationListGenerator
from model.rand import RandStub
from model.kicks import NoKicks, ARSKicks


class TestBasicRules:
    def test01_IPieceSpawnsInTheMiddleWithEvenWidthPlayfield(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test02_IPieceSpawnsInTheMiddleWithOddWidthPlayfield(self):
        random = RandStub([1])
        game = TetrisGame(9, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "--IIII---",
            "---------",
            ".........",
            ".........",
            ".........",
            ".........",
        ]

    def test03_JPieceSpawnsInTheMiddleWithEvenWidthPlayfield(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "---JJJ----",
            "-----J----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test04_JPieceSpawnsInTheMiddleWithOddWidthPlayfield(self):
        random = RandStub([2])
        game = TetrisGame(7, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "--JJJ--",
            "----J--",
            ".......",
            ".......",
            ".......",
            ".......",
        ]

    def test05_LPieceSpawnsInTheMiddle(self):
        random = RandStub([3])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "---LLL----",
            "---L------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test06_OPieceSpawnsInTheMiddleWithEvenPlayfield(self):
        random = RandStub([4])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "----OO----",
            "----OO----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test07_OPieceSpawnsInTheMiddleWithOddPlayfield(self):
        random = RandStub([4])
        game = TetrisGame(11, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "----OO-----",
            "----OO-----",
            "...........",
            "...........",
            "...........",
            "...........",
        ]

    def test08_SPieceSpawnsInTheMiddle(self):
        random = RandStub([5])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "----SS----",
            "---SS-----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test09_ZPieceSpawnsInTheMiddle(self):
        random = RandStub([6])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "---ZZ-----",
            "----ZZ----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test10_TPieceSpawnsInTheMiddle(self):
        random = RandStub([7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.asStringList() == [
            "---TTT----",
            "----T-----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test11_PieceMovesDownAfterTick(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()

        assert game.asStringList() == [
            "----------",
            "---JJJ----",
            ".....J....",
            "..........",
            "..........",
            "..........",
        ]

    def test12_NewPieceSpawnsWhenCurrentPieceIsBlockedByGround(self):
        random = RandStub([2, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.tick()
        game.tick()
        game.tick()
        game.tick()
        game.tick()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "...jjj....",
            ".....j....",
        ]

    def test13_PiecesCanBeStackedOnTopOfEachOther(self):
        random = RandStub([2, 1, 3])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

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
            "---LLL----",
            "---L------",
            "..........",
            "...iiii...",
            "...jjj....",
            ".....j....",
        ]

    def test14_PiecesCanMoveRight(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.moveRight()

        assert game.asStringList() == [
            "----IIII--",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test15_PiecesCanNotMoveRightThroughTheWall(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()

        assert game.asStringList() == [
            "------IIII",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test16_PiecesCanMoveLeft(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.moveLeft()

        assert game.asStringList() == [
            "--IIII----",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test17_PiecesCanNotMoveLeftThroughTheWall(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()

        assert game.asStringList() == [
            "IIII------",
            "----------",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test18_PieceCanSoftDropBetweenTicks(self):
        random = RandStub([2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.softDrop()

        assert game.asStringList() == [
            "----------",
            "---JJJ----",
            ".....J....",
            "..........",
            "..........",
            "..........",
        ]

    def test19_PiecesCanHardDrop(self):
        random = RandStub([2, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "...jjj....",
            ".....j....",
        ]

    def test20_CanClearALine(self):
        random = RandStub([1, 1, 4, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.hardDrop()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "..........",
            "....oo....",
        ]

    def test21_CanClearMultipleLinesAtOnce(self):
        random = RandStub([4, 4, 4, 4, 4, 4])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.hardDrop()

        assert game.asStringList() == [
            "----OO----",
            "----OO----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]


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


class TestSegaRotationSystem:
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


class TestARSKicks:
    def test01_PieceDoesntRotateIfAllKicksFail(self):
        random = RandStub([4, 4, 1])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, ARSKicks)

        # ----------    ----------    ----------    ----------    ----------
        # ----------    -----I----    ------I---    ----I-----    ----------
        # ..........    .....I....    ......I...    ....I.....    ..........
        # ...IIII... -> .....I.... -> ......I... -> ....I..... -> ...IIII...
        # ....oooo..    ....oXoo..    ....ooxo..    ....xooo..    ....oooo..
        # ....oooo..    ....oooo..    ....oooo..    ....oooo..    ....oooo..

        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateRight()

        assert game.asStringList() == [
            "----------",
            "----------",
            "..........",
            "...IIII...",
            "....oooo..",
            "....oooo..",
        ]

    def test02_PieceTriesToKickRightWhenItCantRotate(self):
        random = RandStub([4, 1])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, ARSKicks)

        # ----------    ----------    ----------
        # ----------    -----I----    ------I---
        # ..........    .....I....    ......I...
        # ...IIII... -> .....I.... -> ......I...
        # ....oo....    ....oX....    ....ooI...
        # ....oo....    ....oo....    ....oo....

        game.hardDrop()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateRight()

        assert game.asStringList() == [
            "----------",
            "------I---",
            "......I...",
            "......I...",
            "....ooI...",
            "....oo....",
        ]

    def test03_PieceTriesToKickLeftWhenItCantRotateOrKickRight(self):
        random = RandStub([4, 1])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, ARSKicks)

        # ----------    ----------    ----------
        # ----------    ----I-----    ---I------
        # ..........    ....I.....    ...I......
        # ..IIII.... -> ....I..... -> ...I......
        # ....oo....    ....xo....    ...Ioo....
        # ....oo....    ....oo....    ....oo....

        game.hardDrop()
        game.moveLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.rotateRight()

        assert game.asStringList() == [
            "----------",
            "---I------",
            "...I......",
            "...I......",
            "...Ioo....",
            "....oo....",
        ]

    def test04_IfTheCenterRuleFindsABlockInTheMiddleColumnTheKickDoesntWork(self):
        random = RandStub([4, 1, 1, 3])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, ARSKicks)

        # ----------    ----------    ----------    ----------    ----------
        # ----------    ----------    ----------    ----------    ----------
        # ..........    ..........    ..........    ..........    ..........
        # ....Liiiii -> .....iiiii -> .....xiiii -> .....iiiii -> ....Liiiii
        # ....L...oo    ...LLL..oo    ....LLL.oo    ..LLL...oo    ....L...oo
        # iiiiLL..oo    iiix....oo    iiiiL...oo    iixi....oo    iiiiLL..oo

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.rotateLeft()
        game.softDrop()
        game.softDrop()
        game.softDrop()
        game.moveRight()
        game.softDrop()

        game.rotateRight()

        assert game.asStringList() == [
            "----------",
            "----------",
            "..........",
            ".....Liiii",
            ".....L..oo",
            ".iiiiLL.oo",
        ]

    def test05_IfTheCenterRuleFindsABlockInASideColumnBeforeTheCenterColumnTheKickWorks(self):
        random = RandStub([4, 1, 1, 2])
        game = TetrisGame(10, 4, random, SegaRotationListGenerator, ARSKicks)

        # ----------    ----------    ----------    ----------
        # ----------    ----------    ----------    ----------
        # ..........    ..........    ..........    ..........
        # iiiiJ..... -> iiii...... -> iiii...... -> iiii......
        # oo..J.....    oo.JJJ....    oo..JJJ...    ooJJJ.....
        # oo.JJiiii.    oo...xiii.    oo...ixii.    oo..Jiiii.

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveLeft()
        game.moveLeft()
        game.moveLeft()
        game.hardDrop()

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.rotateRight()
        game.softDrop()
        game.moveRight()
        game.softDrop()
        game.softDrop()
        game.moveLeft()
        game.softDrop()

        game.rotateLeft()

        assert game.asStringList() == [
            "----------",
            "----------",
            "..........",
            "iiii......",
            "ooJJJ.....",
            "oo..Jiiii.",
        ]
