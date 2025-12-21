from model.event_notifier import EventNotifierWithNoArguments, EventNotifierWithOneArgument


class TetrisEventNotifier:
    def __init__(self):
        self.rowClear = EventNotifierWithNoArguments()
        self.doubleRowClear = EventNotifierWithNoArguments()
        self.tripleRowClear = EventNotifierWithNoArguments()
        self.quadrupleRowClear = EventNotifierWithNoArguments()
        self.placedPiece = EventNotifierWithNoArguments()
        self.comboBreak = EventNotifierWithNoArguments()
        self.lost = EventNotifierWithNoArguments()
        self.softDrop = EventNotifierWithNoArguments()
        self.hardDrop = EventNotifierWithOneArgument()
        self.tSpin = EventNotifierWithNoArguments()
        self.miniTSpin = EventNotifierWithNoArguments()

    def attachRowClearEvent(self, event):
        self.rowClear.attach(event)

    def notifyRowClear(self):
        self.rowClear.notify()

    def attachDoubleRowClearEvent(self, event):
        self.doubleRowClear.attach(event)

    def notifyDoubleRowClear(self):
        self.doubleRowClear.notify()

    def attachTripleRowClearEvent(self, event):
        self.tripleRowClear.attach(event)

    def notifyTripleRowClear(self):
        self.tripleRowClear.notify()

    def attachQuadrupleRowClearEvent(self, event):
        self.quadrupleRowClear.attach(event)

    def notifyQuadrupleRowClear(self):
        self.quadrupleRowClear.notify()

    def attachPlacedPieceEvent(self, event):
        self.placedPiece.attach(event)

    def notifyPlacedPiece(self):
        self.placedPiece.notify()

    def attachComboBreakEvent(self, event):
        self.comboBreak.attach(event)

    def notifyComboBreak(self):
        self.comboBreak.notify()

    def attachLostEvent(self, event):
        self.lost.attach(event)

    def notifyLost(self):
        self.lost.notify()

    def attachSoftDropEvent(self, event):
        self.softDrop.attach(event)

    def notifySoftDrop(self):
        self.softDrop.notify()

    def attachHardDropEvent(self, event):
        self.hardDrop.attach(event)

    def notifyHardDrop(self, someBlocks):
        self.hardDrop.notify(someBlocks)

    def attachTSpinEvent(self, event):
        self.tSpin.attach(event)

    def notifyTSpin(self):
        self.tSpin.notify()

    def attachMiniTSpinEvent(self, event):
        self.miniTSpin.attach(event)

    def notifyMiniTSpin(self):
        self.miniTSpin.notify()
