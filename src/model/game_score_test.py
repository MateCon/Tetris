from model.tetris_event_notifier import TetrisEventNotifier
from model.game_score import GameScore
import pytest


class TestGameScore:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.eventNotifier = TetrisEventNotifier()
        self.gameScore = GameScore(self.eventNotifier)

    def test01_ScoreStartsAt0(self):
        assert self.gameScore.score() == 0
        assert self.gameScore.lines() == 0
        assert self.gameScore.level() == 1

    def test02_ScoreIncreasesOnTheFirstRowClear(self):
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.lines() == 1
        assert self.gameScore.score() == 100

    def test03_ScoreIncreasesOnEveryRowClear(self):
        self.eventNotifier.notifyRowClear()
        self.eventNotifier.notifyComboBreak()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.lines() == 2
        assert self.gameScore.score() == 200

    def test04_ScoreIncreaseIsMultipliedByTwoOnTheSecondsLevel(self):
        for _ in range(11):
            self.eventNotifier.notifyRowClear()
            self.eventNotifier.notifyComboBreak()

        assert self.gameScore.score() == 1200
        assert self.gameScore.level() == 2

    def test05_ScoreIncreaseIsMultipliedByLevel(self):
        for _ in range(21):
            self.eventNotifier.notifyRowClear()
            self.eventNotifier.notifyComboBreak()

        assert self.gameScore.score() == 3300
        assert self.gameScore.level() == 3

    def test06_ScoreInscreasesOnDoubleRowClear(self):
        self.eventNotifier.notifyDoubleRowClear()

        assert self.gameScore.score() == 300

    def test07_ScoreInscreasesOnTripleRowClear(self):
        self.eventNotifier.notifyTripleRowClear()

        assert self.gameScore.score() == 500

    def test08_ScoreInscreasesOnQuadrupleRowClear(self):
        self.eventNotifier.notifyQuadrupleRowClear()

        assert self.gameScore.score() == 800

    def test09_BonusScoreIsAwardedOnTwoConsecutiveClears(self):
        self.eventNotifier.notifyRowClear()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 250

    def test10_BonusScoreIsStackedOnConsecutiveClears(self):
        self.eventNotifier.notifyRowClear()
        self.eventNotifier.notifyRowClear()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 450

    def test11_BonusScoreIsMultipliedByCurrentLevel(self):
        for _ in range(10):
            self.eventNotifier.notifyComboBreak()
            self.eventNotifier.notifyRowClear()

        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 1300

    def test12_SoftDropAlwaysGiveOnePoint(self):
        self.eventNotifier.notifySoftDrop()

        assert self.gameScore.score() == 1

    def test13_HardDropGivesTwoPointsPerBlockDropped(self):
        self.eventNotifier.notifyHardDrop(5)

        assert self.gameScore.score() == 10

    def test14_TSpinWithNoRowClear(self):
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyPlacedPiece()

        assert self.gameScore.score() == 400

    def test15_TSpinDoesNotApplyBeforeAPlacedPiece(self):
        self.eventNotifier.notifyTSpin()

        assert self.gameScore.score() == 0

    def test16_TSpinWithRowClear(self):
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 800

    def test17_TSpinWithDoubleRowClear(self):
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyDoubleRowClear()

        assert self.gameScore.score() == 1200

    def test18_TSpinWithTripleRowClear(self):
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyTripleRowClear()

        assert self.gameScore.score() == 1600

    def test19_SpinsAreAffectedByMultipliers(self):
        for _ in range(10):
            self.eventNotifier.notifyRowClear()
            self.eventNotifier.notifyComboBreak()

        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyTripleRowClear()

        assert self.gameScore.score() == 1000 + 1600 * 2

    def test20_MiniTSpinWithNoRowClear(self):
        self.eventNotifier.notifyMiniTSpin()
        self.eventNotifier.notifyPlacedPiece()

        assert self.gameScore.score() == 100

    def test21_MiniTSpinWithRowClear(self):
        self.eventNotifier.notifyMiniTSpin()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 200

    def test22_MiniTSpinWithDoubleRowClear(self):
        self.eventNotifier.notifyMiniTSpin()
        self.eventNotifier.notifyDoubleRowClear()

        assert self.gameScore.score() == 400

    def test23_IfTSpinWasTheLastSpinThenTSpinIsApplied(self):
        self.eventNotifier.notifyMiniTSpin()
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyPlacedPiece()

        assert self.gameScore.score() == 400

    def test24_IfMiniTSpinWasTheLastSpinThenMiniTSpinIsApplied(self):
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyMiniTSpin()
        self.eventNotifier.notifyPlacedPiece()

        assert self.gameScore.score() == 100

    def test25_SpinsOnlyWorkForTheInmediatePiecePlacement(self):
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyPlacedPiece()
        self.eventNotifier.notifyPlacedPiece()

        assert self.gameScore.score() == 400

    def test26_CombosDoNotStackForPlacedPieces(self):
        self.eventNotifier.notifyPlacedPiece()
        self.eventNotifier.notifyPlacedPiece()

        assert self.gameScore.score() == 0

    def test27_BackToBackTetrisMovesAwards50PercentAdditionalScore(self):
        self.eventNotifier.notifyQuadrupleRowClear()
        self.eventNotifier.notifyComboBreak()
        self.eventNotifier.notifyQuadrupleRowClear()

        assert self.gameScore.score() == 800 + 1200

    def test28_BackToBackDifficultMovesAwards50PercentAdditionalScore(self):
        self.eventNotifier.notifyTSpin()
        self.eventNotifier.notifyRowClear()
        self.eventNotifier.notifyComboBreak()
        self.eventNotifier.notifyMiniTSpin()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 800 + 300

    def test29_NonBackToBackDifficultMovesDoNotAward50PercentAdditionalScore(self):
        self.eventNotifier.notifyQuadrupleRowClear()
        self.eventNotifier.notifyComboBreak()
        self.eventNotifier.notifyRowClear()
        self.eventNotifier.notifyComboBreak()
        self.eventNotifier.notifyQuadrupleRowClear()

        assert self.gameScore.score() == 800 + 100 + 800

    def test30_APiecePlacementDoesNotCancelBackToBackMoves(self):
        self.eventNotifier.notifyQuadrupleRowClear()
        self.eventNotifier.notifyComboBreak()
        self.eventNotifier.notifyPlacedPiece()
        self.eventNotifier.notifyQuadrupleRowClear()

        assert self.gameScore.score() == 800 + 1200

    def test31_SingleLinePerfectClearBonus(self):
        self.eventNotifier.notifyPerfectClear()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 100 + 800

    def test32_PerfectClearBonusesAreAffectedByLevel(self):
        for _ in range(10):
            self.eventNotifier.notifyRowClear()
            self.eventNotifier.notifyComboBreak()

        self.eventNotifier.notifyPerfectClear()
        self.eventNotifier.notifyRowClear()

        assert self.gameScore.score() == 1000 + (100 + 800) * 2

    def test33_DoubleLinePerfectClearBonus(self):
        self.eventNotifier.notifyPerfectClear()
        self.eventNotifier.notifyDoubleRowClear()

        assert self.gameScore.score() == 300 + 1200

    def test34_TripleLinePerfectClearBonus(self):
        self.eventNotifier.notifyPerfectClear()
        self.eventNotifier.notifyTripleRowClear()

        assert self.gameScore.score() == 500 + 1800

    def test35_TetrisPerfectClearBonus(self):
        self.eventNotifier.notifyPerfectClear()
        self.eventNotifier.notifyQuadrupleRowClear()

        assert self.gameScore.score() == 800 + 2000

    def test36_BackToBackTetrisPerfectClearBonus(self):
        self.eventNotifier.notifyQuadrupleRowClear()
        self.eventNotifier.notifyComboBreak()
        self.eventNotifier.notifyPerfectClear()
        self.eventNotifier.notifyQuadrupleRowClear()

        assert self.gameScore.score() == 800 + 1200 + 3200
