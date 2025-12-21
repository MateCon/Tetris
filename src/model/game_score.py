class GameScore:
    def __init__(self, anEventNotifier):
        self.value = 0
        self.linesCleared = 0
        self.combo = 0
        self.tSpin = False
        self.miniTSpin = False
        self.tSpinScores = [400, 800, 1200, 1600]
        self.miniTSpinScores = [100, 200, 400]
        self.lastMoveWasDifficult = False
        self.isPerfectClear = False
        self.perfectClearBonusScores = [800, 1200, 1800, 2000]
        self.perfectClearBackToBackTetrisScore = 3200

        def addScore(aScore):
            self.value += aScore

        def isMoveDifficult(aNumberOfLines):
            return aNumberOfLines == 4 or ((self.tSpin or self.miniTSpin) and aNumberOfLines >= 1)

        def modifyScoreIfTSpin(aNumberOfLines, aScore):
            if self.tSpin:
                aScore = self.tSpinScores[aNumberOfLines]
            if self.miniTSpin:
                aScore = self.miniTSpinScores[aNumberOfLines]
            return aScore

        def modifyScoreIfBackToBack(aNumberOfLines, aScore):
            isCurrentMoveDifficult = isMoveDifficult(aNumberOfLines)
            if isMoveDifficult(aNumberOfLines) and self.lastMoveWasDifficult:
                aScore = aScore * 3 // 2
            if (not self.tSpin) and (not self.miniTSpin) and aNumberOfLines == 0 and self.lastMoveWasDifficult:
                self.lastMoveWasDifficult = True
            else:
                self.lastMoveWasDifficult = isCurrentMoveDifficult
            return aScore

        def perfectClear():
            self.isPerfectClear = True

        def calculateBonus(aNumberOfLines, lastMovewasDifficult):
            if self.isPerfectClear and aNumberOfLines == 4 and lastMovewasDifficult:
                return self.perfectClearBackToBackTetrisScore
            if self.isPerfectClear:
                return self.perfectClearBonusScores[aNumberOfLines - 1]
            return 0

        def clearLines(aNumberOfLines, aScore):
            lastMoveWasDifficult = self.lastMoveWasDifficult
            aScore = modifyScoreIfTSpin(aNumberOfLines, aScore)
            aScore = modifyScoreIfBackToBack(aNumberOfLines, aScore)
            bonusScore = calculateBonus(aNumberOfLines, lastMoveWasDifficult)

            addScore((aScore + bonusScore + self.combo * 50) * self.level())
            self.linesCleared += aNumberOfLines
            self.combo += 1

        def resetCombo():
            self.combo = 0

        def tSpin():
            self.tSpin = True
            self.miniTSpin = False

        def miniTSpin():
            self.miniTSpin = True
            self.tSpin = False

        def resetTSpin():
            clearLines(0, 0)
            resetCombo()
            self.tSpin = False
            self.miniTSpin = False

        anEventNotifier.attachRowClearEvent(lambda: clearLines(1, 100))
        anEventNotifier.attachDoubleRowClearEvent(lambda: clearLines(2, 300))
        anEventNotifier.attachTripleRowClearEvent(lambda: clearLines(3, 500))
        anEventNotifier.attachQuadrupleRowClearEvent(lambda: clearLines(4, 800))
        anEventNotifier.attachComboBreakEvent(resetCombo)

        anEventNotifier.attachTSpinEvent(lambda: tSpin())
        anEventNotifier.attachMiniTSpinEvent(lambda: miniTSpin())
        anEventNotifier.attachPlacedPieceEvent(lambda: resetTSpin())

        anEventNotifier.attachPerfectClearEvent(perfectClear)

        anEventNotifier.attachSoftDropEvent(lambda: addScore(1))
        anEventNotifier.attachHardDropEvent(lambda blocksDropped: addScore(2 * blocksDropped))

    def lines(self):
        return self.linesCleared

    def level(self):
        return self.lines() // 10 + 1

    def score(self):
        return self.value
