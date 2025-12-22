from tetris_model.rotation_list import RotationList
from tetris_model.tetris_game import TetrisGame
from tetris_model.rotation_list_generator import NintendoRotationListGenerator
from tetris_model.rand import RandStub
from tetris_model.kicks import NoKicks


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

    def test22_NextPieceIsKnownBeforeLandingTheCurrentOne(self):
        random = RandStub([4, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.getNextPiece().activeCharacter() == "I"

    def test23_EntireBagIsKnown(self):
        random = RandStub([4, 2, 1, 5, 7, 6, 3])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        bag = game.getCurrentBag()

        assert bag.isActiveCharacterAt(4, "T")

    def test24_NextPieceIsKnownBeforeLandingTheLastOneInTheBag(self):
        random = RandStub([1, 1, 1, 1, 1, 1, 1, 2])
        game = TetrisGame(10, 20, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()
        game.hardDrop()
        game.hardDrop()
        game.hardDrop()
        game.hardDrop()
        game.hardDrop()

        assert game.getNextPiece().activeCharacter() == "J"

    def test25_NextBagIsKnownSinceTheCurrentOneIsConsumed(self):
        random = RandStub([1, 1, 1, 1, 1, 1, 1, 2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        bag = game.getNextBag()

        assert bag.isActiveCharacterAt(0, "J")

    def test26_PieceCanPrintItSelf(self):
        random = RandStub([1,7])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.getNextPiece().asStringList() == [
            "....",
            "TTT.",
            ".T..",
        ]
        
    def test27_IPieceIsPrintedInTheMiddle(self):
        random = RandStub([7,1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.getNextPiece().asStringList() == [
            "....",
            "IIII",
            "....",
        ]

    def test28_NextSixPiecesAreKnown(self):
        random = RandStub([1, 2, 3, 4, 5, 6, 7, 1, 2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()
        game.hardDrop()

        nextSix = game.getNextSix()

        assert len(nextSix) == 6
        assert nextSix[0].activeCharacter() == "O"
        assert nextSix[1].activeCharacter() == "S"
        assert nextSix[2].activeCharacter() == "Z"
        assert nextSix[3].activeCharacter() == "T"
        assert nextSix[4].activeCharacter() == "I"
        assert nextSix[5].activeCharacter() == "J"

    def test29_WhenPlayerLosesByPlacingABlockInTheVanishingZoneNoNewPieceSpawns(self):
        random = RandStub([4, 4, 4, 4, 4, 4])
        game = TetrisGame(10, 3, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()
        game.hardDrop()

        assert game.asStringList() == [
            "----------",
            "----oo----",
            "....oo....",
            "....oo....",
            "....oo....",
        ]

    def test30_PlayerDoesntLoseByPlacingAPieceUpToTheVanishingZone(self):
        random = RandStub([4, 4, 4, 4, 4, 4])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()
        game.hardDrop()

        assert game.asStringList() == [
            "----OO----",
            "----OO----",
            "....oo....",
            "....oo....",
            "....oo....",
            "....oo....",
        ]

    def test31_PlayerLosesEvenWhenALineWillBeCleared(self):
        random = RandStub([4, 4])
        game = TetrisGame(2, 1, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()

        assert game.asStringList() == [
            "--",
            "oo",
            "oo",
        ]

    def test32_GameKnowsItsActivePieceCharacter(self):
        random = RandStub([1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        assert game.activeCharacter() == 'I'

    def test33_BoardCanPreviewTheGhostPiece(self):
        random = RandStub([2, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()

        assert game.asStringListWithGhostPiece() == [
            "---IIII---",
            "----------",
            "..........",
            "...####...",
            "...jjj....",
            ".....j....",
        ]

    def test34_GhostPieceDoesNotAppearOverCurrentPiece(self):
        random = RandStub([1, 2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()
        game.softDrop()
        game.softDrop()

        assert game.asStringListWithGhostPiece() == [
            "----------",
            "----------",
            "...JJJ....",
            "...##J....",
            ".....#....",
            "...iiii...",
        ]

    def test35_HoldingAPieceWithAnEmptyQueueGoesToTheNextPiece(self):
        random = RandStub([1, 4, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hold()

        assert game.asStringList() == [
            "----OO----",
            "----OO----",
            "..........",
            "..........",
            "..........",
            "..........",
        ]

    def test36_HoldingAPieceWithANonEmptyQueueSwapsThePieces(self):
        random = RandStub([1, 4, 7, 2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hold()
        game.hardDrop()
        game.hold()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "....oo....",
            "....oo....",
        ]

    def test37_HoldingAPieceResetsItToItsOriginalPosition(self):
        random = RandStub([1, 4, 7, 2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.softDrop()
        game.hold()
        game.hardDrop()
        game.hold()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "....oo....",
            "....oo....",
        ]

    def test38_HoldingAPieceResetsItToItsOriginalRotation(self):
        random = RandStub([1, 4, 7, 2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateRight()
        game.hold()
        game.hardDrop()
        game.hold()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "....oo....",
            "....oo....",
        ]

    def test39_HoldingAPieceResetsItToItsOriginalRotationWhenStored(self):
        random = RandStub([2, 1])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.rotateRight()
        game.hold()

        assert game.getHeldPiece().asStringList() == [
            "....",
            "JJJ.",
            "..J.",
        ]

    def test40_APieceCanNotBeHeldOnceRemovedFromHoldingQueue(self):
        random = RandStub([1, 4, 2])
        game = TetrisGame(10, 4, random, NintendoRotationListGenerator, NoKicks)

        game.hold()
        game.hardDrop()
        game.hold()
        game.hold()

        assert game.asStringList() == [
            "---IIII---",
            "----------",
            "..........",
            "..........",
            "....oo....",
            "....oo....",
        ]

    def test41_GameCanBeLostWithABlockAboveTheVanishZone(self):
        random = RandStub([4, 1, 1])
        game = TetrisGame(6, 2, random, NintendoRotationListGenerator, NoKicks)

        game.hardDrop()
        game.rotateRight()
        game.tick()
        game.tick()

        assert game.asStringList() == [
            "---i--",
            "---i--",
            "..oo..",
            "..oo..",
        ]

    def test42_CanNotHoldAfterGameIsLost(self):
        random = RandStub([4, 4, 4, 4])
        game = TetrisGame(10, 1, random, NintendoRotationListGenerator, NoKicks)

        game.moveRight()
        game.moveRight()
        game.hardDrop()

        game.hold()

        assert game.asStringList() == [
            "----------",
            "------oo--",
            "......oo..",
        ]

    def test42_HoldRightAfterFirstHold(self):
        random = RandStub([4, 1])
        game = TetrisGame(10, 1, random, NintendoRotationListGenerator, NoKicks)

        game.hold()
        game.hold()

        assert game.getHeldPiece().activeCharacter() == "I"
