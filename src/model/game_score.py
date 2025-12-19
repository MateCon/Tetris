class GameScore:
    def __init__(self, anEventNotifier):
        self.value = 0
        self.linesCleared = 0
        self.combo = 0

        def clearLines(aNumberOfLines, aScore):
            self.value += (aScore + self.combo * 50) * self.level()
            self.linesCleared += aNumberOfLines
            self.combo += 1

        def resetCombo():
            self.combo = 0

        anEventNotifier.attachRowClearEvent(lambda: clearLines(1, 100))
        anEventNotifier.attachDoubleRowClearEvent(lambda: clearLines(2, 300))
        anEventNotifier.attachTripleRowClearEvent(lambda: clearLines(3, 500))
        anEventNotifier.attachQuadrupleRowClearEvent(lambda: clearLines(4, 800))
        anEventNotifier.attachComboBreakEvent(lambda: resetCombo())

    def lines(self):
        return self.linesCleared

    def level(self):
        return self.lines() // 10 + 1

    def score(self):
        return self.value
