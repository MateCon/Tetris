from model.tetris_game import TetrisGame
from model.rotation_list_generator import SegaRotationListGenerator
from model.rand import RandStub
from model.kicks import ARSKicks


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
