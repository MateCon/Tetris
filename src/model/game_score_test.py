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
